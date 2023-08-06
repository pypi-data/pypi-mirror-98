# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Compute the residual cosmic-ray contamination
"""
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import numpy as np
import healpy

from fermipy.skymap import HpxMap
from fermipy import fits_utils
from fermipy.utils import load_yaml
from fermipy.jobs.file_archive import FileFlags
from fermipy.jobs.scatter_gather import ScatterGather
from fermipy.jobs.slac_impl import make_nfs_path
from fermipy.jobs.link import Link
from fermipy.jobs.chain import Chain

from fermipy.diffuse.binning import Component
from fermipy.diffuse.name_policy import NameFactory
from fermipy.diffuse import defaults as diffuse_defaults

from fermipy.diffuse.gt_split_and_mktime import SplitAndMktimeChain


NAME_FACTORY = NameFactory()
NAME_FACTORY_CLEAN = NameFactory()
NAME_FACTORY_DIRTY = NameFactory()


class ResidualCR(Link):
    """Small class to analyze the residual cosmic-ray contaimination.
    """
    appname = 'fermipy-residual-cr'
    linkname_default = 'residual-cr'
    usage = '%s [options]' % (appname)
    description = "Compute the residual cosmic-ray contamination"

    default_options = dict(ccube_dirty=diffuse_defaults.residual_cr['ccube_dirty'],
                           ccube_clean=diffuse_defaults.residual_cr['ccube_clean'],
                           bexpcube_dirty=diffuse_defaults.residual_cr['bexpcube_dirty'],
                           bexpcube_clean=diffuse_defaults.residual_cr['bexpcube_clean'],
                           hpx_order=diffuse_defaults.gtopts['hpx_order'],
                           outfile=diffuse_defaults.gtopts['outfile'],
                           select_factor=diffuse_defaults.residual_cr['select_factor'],
                           mask_factor=diffuse_defaults.residual_cr['mask_factor'],
                           sigma=diffuse_defaults.residual_cr['sigma'],
                           full_output=diffuse_defaults.residual_cr['full_output'],
                           clobber=diffuse_defaults.gtopts['clobber'])

    default_file_args = dict(ccube_dirty=FileFlags.input_mask,
                             bexpcube_dirty=FileFlags.input_mask,
                             ccube_clean=FileFlags.input_mask,
                             bexpcube_clean=FileFlags.input_mask,
                             outfile=FileFlags.output_mask)

    __doc__ += Link.construct_docstring(default_options)

    @staticmethod
    def _match_cubes(ccube_clean, ccube_dirty,
                     bexpcube_clean, bexpcube_dirty,
                     hpx_order):
        """ Match the HEALPIX scheme and order of all the input cubes

        return a dictionary of cubes with the same HEALPIX scheme and order
        """
        if hpx_order == ccube_clean.hpx.order:
            ccube_clean_at_order = ccube_clean
        else:
            ccube_clean_at_order = ccube_clean.ud_grade(hpx_order, preserve_counts=True)

        if hpx_order == ccube_dirty.hpx.order:
            ccube_dirty_at_order = ccube_dirty
        else:
            ccube_dirty_at_order = ccube_dirty.ud_grade(hpx_order, preserve_counts=True)

        if hpx_order == bexpcube_clean.hpx.order:
            bexpcube_clean_at_order = bexpcube_clean
        else:
            bexpcube_clean_at_order = bexpcube_clean.ud_grade(hpx_order, preserve_counts=True)

        if hpx_order == bexpcube_dirty.hpx.order:
            bexpcube_dirty_at_order = bexpcube_dirty
        else:
            bexpcube_dirty_at_order = bexpcube_dirty.ud_grade(hpx_order, preserve_counts=True)

        if ccube_dirty_at_order.hpx.nest != ccube_clean.hpx.nest:
            ccube_dirty_at_order = ccube_dirty_at_order.swap_scheme()

        if bexpcube_clean_at_order.hpx.nest != ccube_clean.hpx.nest:
            bexpcube_clean_at_order = bexpcube_clean_at_order.swap_scheme()

        if bexpcube_dirty_at_order.hpx.nest != ccube_clean.hpx.nest:
            bexpcube_dirty_at_order = bexpcube_dirty_at_order.swap_scheme()

        ret_dict = dict(ccube_clean=ccube_clean_at_order,
                        ccube_dirty=ccube_dirty_at_order,
                        bexpcube_clean=bexpcube_clean_at_order,
                        bexpcube_dirty=bexpcube_dirty_at_order)
        return ret_dict

    @staticmethod
    def _compute_intensity(ccube, bexpcube):
        """ Compute the intensity map
        """
        bexp_data = np.sqrt(bexpcube.data[0:-1, 0:] * bexpcube.data[1:, 0:])
        intensity_data = ccube.data / bexp_data
        intensity_map = HpxMap(intensity_data, ccube.hpx)
        return intensity_map

    @staticmethod
    def _compute_mean(map1, map2):
        """ Make a map that is the mean of two maps
        """
        data = (map1.data + map2.data) / 2.
        return HpxMap(data, map1.hpx)

    @staticmethod
    def _compute_ratio(top, bot):
        """ Make a map that is the ratio of two maps
        """
        data = np.where(bot.data > 0, top.data / bot.data, 0.)
        return HpxMap(data, top.hpx)

    @staticmethod
    def _compute_diff(map1, map2):
        """ Make a map that is the difference of two maps
        """
        data = map1.data - map2.data
        return HpxMap(data, map1.hpx)

    @staticmethod
    def _compute_product(map1, map2):
        """ Make a map that is the product of two maps
        """
        data = map1.data * map2.data
        return HpxMap(data, map1.hpx)

    @staticmethod
    def _compute_counts_from_intensity(intensity, bexpcube):
        """ Make the counts map from the intensity
        """
        data = intensity.data * np.sqrt(bexpcube.data[1:] * bexpcube.data[0:-1])
        return HpxMap(data, intensity.hpx)

    @staticmethod
    def _compute_counts_from_model(model, bexpcube):
        """ Make the counts maps from teh mdoe
        """
        data = model.data * bexpcube.data
        ebins = model.hpx.ebins
        ratio = ebins[1:] / ebins[0:-1]
        half_log_ratio = np.log(ratio) / 2.
        int_map = ((data[0:-1].T * ebins[0:-1]) + (data[1:].T * ebins[1:])) * half_log_ratio
        return HpxMap(int_map.T, model.hpx)

    @staticmethod
    def _make_bright_pixel_mask(intensity_mean, mask_factor=5.0):
        """ Make of mask of all the brightest pixels """
        mask = np.zeros((intensity_mean.data.shape), bool)
        nebins = len(intensity_mean.data)
        sum_intensity = intensity_mean.data.sum(0)
        mean_intensity = sum_intensity.mean()
        for i in range(nebins):
            mask[i, 0:] = sum_intensity > (mask_factor * mean_intensity)
        return HpxMap(mask, intensity_mean.hpx)

    @staticmethod
    def _get_aeff_corrections(intensity_ratio, mask):
        """ Compute a correction for the effective area from the brighter pixesl
        """
        nebins = len(intensity_ratio.data)
        aeff_corrections = np.zeros((nebins))
        for i in range(nebins):
            bright_pixels_intensity = intensity_ratio.data[i][mask.data[i]]
            mean_bright_pixel = bright_pixels_intensity.mean()
            aeff_corrections[i] = 1. / mean_bright_pixel

        print("Aeff correction: ", aeff_corrections)
        return aeff_corrections

    @staticmethod
    def _apply_aeff_corrections(intensity_map, aeff_corrections):
        """ Multipy a map by the effective area correction
        """
        data = aeff_corrections * intensity_map.data.T
        return HpxMap(data.T, intensity_map.hpx)

    @staticmethod
    def _fill_masked_intensity_resid(intensity_resid, bright_pixel_mask):
        """ Fill the pixels used to compute the effective area correction with the mean intensity
        """
        filled_intensity = np.zeros((intensity_resid.data.shape))
        nebins = len(intensity_resid.data)
        for i in range(nebins):
            masked = bright_pixel_mask.data[i]
            unmasked = np.invert(masked)
            mean_intensity = intensity_resid.data[i][unmasked].mean()
            filled_intensity[i] = np.where(masked, mean_intensity, intensity_resid.data[i])
        return HpxMap(filled_intensity, intensity_resid.hpx)

    @staticmethod
    def _smooth_hpx_map(hpx_map, sigma):
        """ Smooth a healpix map using a Gaussian
        """
        if hpx_map.hpx.ordering == "NESTED":
            ring_map = hpx_map.swap_scheme()
        else:
            ring_map = hpx_map
        ring_data = ring_map.data.copy()
        nebins = len(hpx_map.data)
        smoothed_data = np.zeros((hpx_map.data.shape))
        for i in range(nebins):
            smoothed_data[i] = healpy.sphtfunc.smoothing(
                ring_data[i], sigma=np.radians(sigma), verbose=False)

        smoothed_data.clip(0., 1e99)
        smoothed_ring_map = HpxMap(smoothed_data, ring_map.hpx)
        if hpx_map.hpx.ordering == "NESTED":
            return smoothed_ring_map.swap_scheme()
        return smoothed_ring_map

    @staticmethod
    def _intergral_to_differential(hpx_map, gamma=-2.0):
        """ Convert integral quantity to differential quantity

        Here we are assuming the spectrum is a powerlaw with index gamma and we
        are using log-log-quadrature to compute the integral quantities.
        """
        nebins = len(hpx_map.data)
        diff_map = np.zeros((nebins + 1, hpx_map.hpx.npix))
        ebins = hpx_map.hpx.ebins
        ratio = ebins[1:] / ebins[0:-1]
        half_log_ratio = np.log(ratio) / 2.
        ratio_gamma = np.power(ratio, gamma)
        #ratio_inv_gamma = np.power(ratio, -1. * gamma)

        diff_map[0] = hpx_map.data[0] / ((ebins[0] + ratio_gamma[0] * ebins[1]) * half_log_ratio[0])
        for i in range(nebins):
            diff_map[i + 1] = (hpx_map.data[i] / (ebins[i + 1] *
                                                  half_log_ratio[i])) - (diff_map[i] / ratio[i])
        return HpxMap(diff_map, hpx_map.hpx)

    @staticmethod
    def _differential_to_integral(hpx_map):
        """ Convert a differential map to an integral map

        Here we are using log-log-quadrature to compute the integral quantities.
        """
        ebins = hpx_map.hpx.ebins
        ratio = ebins[1:] / ebins[0:-1]
        half_log_ratio = np.log(ratio) / 2.
        int_map = ((hpx_map.data[0:-1].T * ebins[0:-1]) +
                   (hpx_map.data[1:].T * ebins[1:])) * half_log_ratio
        return HpxMap(int_map.T, hpx_map.hpx)

    def run_analysis(self, argv):
        """Run this analysis"""
        args = self._parser.parse_args(argv)

        # Read the input maps
        ccube_dirty = HpxMap.create_from_fits(args.ccube_dirty, hdu='SKYMAP')
        bexpcube_dirty = HpxMap.create_from_fits(args.bexpcube_dirty, hdu='HPXEXPOSURES')
        ccube_clean = HpxMap.create_from_fits(args.ccube_clean, hdu='SKYMAP')
        bexpcube_clean = HpxMap.create_from_fits(args.bexpcube_clean, hdu='HPXEXPOSURES')

        # Decide what HEALPix order to work at
        if args.hpx_order:
            hpx_order = args.hpx_order
        else:
            hpx_order = ccube_dirty.hpx.order

        # Cast all the input maps to match ccube_clean
        cube_dict = ResidualCR._match_cubes(ccube_clean, ccube_dirty,
                                            bexpcube_clean, bexpcube_dirty, hpx_order)

        # Intenstiy maps
        intensity_clean = ResidualCR._compute_intensity(cube_dict['ccube_clean'],
                                                        cube_dict['bexpcube_clean'])
        intensity_dirty = ResidualCR._compute_intensity(cube_dict['ccube_dirty'],
                                                        cube_dict['bexpcube_dirty'])
        # Mean & ratio of intensity maps
        intensity_mean = ResidualCR._compute_mean(intensity_dirty,
                                                  intensity_clean)
        intensity_ratio = ResidualCR._compute_ratio(intensity_dirty,
                                                    intensity_clean)
        # Selecting the bright pixels for Aeff correction and to mask when filling output map
        bright_pixel_select = ResidualCR._make_bright_pixel_mask(intensity_mean,
                                                                 args.select_factor)
        bright_pixel_mask = ResidualCR._make_bright_pixel_mask(intensity_mean,
                                                               args.mask_factor)
        # Compute thte Aeff corrections using the brightest pixels
        aeff_corrections = ResidualCR._get_aeff_corrections(intensity_ratio,
                                                            bright_pixel_select)
        # Apply the Aeff corrections and get the intensity residual
        corrected_dirty = ResidualCR._apply_aeff_corrections(intensity_dirty,
                                                             aeff_corrections)
        corrected_ratio = ResidualCR._compute_ratio(corrected_dirty,
                                                    intensity_clean)
        intensity_resid = ResidualCR._compute_diff(corrected_dirty,
                                                   intensity_clean)
        # Replace the masked pixels with the map mean to avoid features associates with sources
        filled_resid = ResidualCR._fill_masked_intensity_resid(intensity_resid,
                                                               bright_pixel_mask)
        # Smooth the map
        smooth_resid = ResidualCR._smooth_hpx_map(filled_resid,
                                                  args.sigma)
        # Convert to a differential map
        out_model = ResidualCR._intergral_to_differential(smooth_resid)

        # Make the ENERGIES HDU
        out_energies = ccube_dirty.hpx.make_energies_hdu()

        # Write the maps
        cubes = dict(SKYMAP=out_model)
        fits_utils.write_maps(None, cubes,
                              args.outfile, energy_hdu=out_energies)

        if args.full_output:
            # Some diagnostics
            check = ResidualCR._differential_to_integral(out_model)
            check_resid = ResidualCR._compute_diff(smooth_resid, check)
            counts_resid =\
                ResidualCR._compute_counts_from_intensity(intensity_resid,
                                                          cube_dict['bexpcube_dirty'])
            pred_counts\
                = ResidualCR._compute_counts_from_model(out_model,
                                                        cube_dict['bexpcube_dirty'])
            pred_resid = ResidualCR._compute_diff(pred_counts, counts_resid)

            out_ebounds = ccube_dirty.hpx.make_energy_bounds_hdu()
            cubes = dict(INTENSITY_CLEAN=intensity_clean,
                         INTENSITY_DIRTY=intensity_dirty,
                         INTENSITY_RATIO=intensity_ratio,
                         CORRECTED_DIRTY=corrected_dirty,
                         CORRECTED_RATIO=corrected_ratio,
                         INTENSITY_RESID=intensity_resid,
                         PIXEL_SELECT=bright_pixel_select,
                         PIXEL_MASK=bright_pixel_mask,
                         FILLED_RESID=filled_resid,
                         SMOOTH_RESID=smooth_resid,
                         CHECK=check,
                         CHECK_RESID=check_resid,
                         COUNTS_RESID=counts_resid,
                         PRED_COUNTS=pred_counts,
                         PRED_RESID=pred_resid)

            fits_utils.write_maps(None, cubes,
                                  args.outfile.replace('.fits', '_full.fits'),
                                  energy_hdu=out_ebounds)


class ResidualCR_SG(ScatterGather):
    """Small class to generate configurations for this script
    """
    appname = 'fermipy-residual-cr-sg'
    usage = "%s [options]" % (appname)
    description = "Compute the residual cosmic-ray contamination"
    clientclass = ResidualCR

    job_time = 300

    default_options = dict(comp=diffuse_defaults.diffuse['comp'],
                           data=diffuse_defaults.diffuse['data'],
                           mktimefilter=diffuse_defaults.diffuse['mktimefilter'],
                           hpx_order=diffuse_defaults.gtopts['hpx_order'],
                           clean=diffuse_defaults.residual_cr['clean'],
                           dirty=diffuse_defaults.residual_cr['dirty'],
                           select_factor=diffuse_defaults.residual_cr['select_factor'],
                           mask_factor=diffuse_defaults.residual_cr['mask_factor'],
                           sigma=diffuse_defaults.residual_cr['sigma'],
                           full_output=diffuse_defaults.residual_cr['full_output'])

    __doc__ += Link.construct_docstring(default_options)

    def build_job_configs(self, args):
        """Hook to build job configurations
        """
        job_configs = {}

        components = Component.build_from_yamlfile(args['comp'])
        NAME_FACTORY.update_base_dict(args['data'])
        NAME_FACTORY_CLEAN.update_base_dict(args['data'])
        NAME_FACTORY_DIRTY.update_base_dict(args['data'])

        NAME_FACTORY_CLEAN.base_dict['evclass'] = args['clean']
        NAME_FACTORY_DIRTY.base_dict['evclass'] = args['dirty']

        for comp in components:
            zcut = "zmax%i" % comp.zmax
            key = comp.make_key('{ebin_name}_{evtype_name}')
            name_keys = dict(zcut=zcut,
                             ebin=comp.ebin_name,
                             psftype=comp.evtype_name,
                             coordsys=comp.coordsys,
                             irf_ver=NAME_FACTORY.irf_ver(),
                             mktime=args['mktimefilter'],
                             fullpath=True)
            outfile = NAME_FACTORY.residual_cr(**name_keys)
            if args['hpx_order']:
                hpx_order = min(comp.hpx_order, args['hpx_order'])
            else:
                hpx_order = comp.hpx_order
            job_configs[key] = dict(bexpcube_dirty=NAME_FACTORY_DIRTY.bexpcube(**name_keys),
                                    ccube_dirty=NAME_FACTORY_DIRTY.ccube(**name_keys),
                                    bexpcube_clean=NAME_FACTORY_CLEAN.bexpcube(**name_keys),
                                    ccube_clean=NAME_FACTORY_CLEAN.ccube(**name_keys),
                                    outfile=outfile,
                                    hpx_order=hpx_order,
                                    full_output=args['full_output'],
                                    logfile=make_nfs_path(outfile.replace('.fits', '.log')))

        return job_configs


class ResidualCRChain(Chain):
    """Chain to preform analysis of residual cosmic-ray contamination

    This chain consists of:

    split-and-mktime : `SplitAndMktimeChain`
        Chain to bin up the data and make exposure cubes    

    residual-cr : `ResidualCR`
        Residual CR analysis

    """
    appname = 'fermipy-residual-cr-chain'
    linkname_default = 'residual-cr-chain'
    usage = '%s [options]' % (appname)
    description = 'Run residual cosmic ray analysis'

    default_options = dict(config=diffuse_defaults.diffuse['config'])

    __doc__ += Link.construct_docstring(default_options)

    def __init__(self, **kwargs):
        """C'tor
        """
        super(ResidualCRChain, self).__init__(**kwargs)
        self.comp_dict = None

    def _map_arguments(self, args):
        """Map from the top-level arguments to the arguments provided to
        the indiviudal links """

        config_yaml = args['config']
        config_dict = load_yaml(config_yaml)

        data = config_dict.get('data')
        comp = config_dict.get('comp')
        dry_run = args.get('dry_run', False)

        self._set_link('prepare', SplitAndMktimeChain,
                       comp=comp, data=data,
                       ft1file=config_dict['ft1file'],
                       ft2file=config_dict['ft2file'],
                       hpx_order_ccube=config_dict.get('hpx_order_ccube', 7),
                       hpx_order_expcube=config_dict.get('hpx_order_expcube', 7),
                       mktime=config_dict.get('mktimefitler', None),
                       do_ltsum=config_dict.get('do_ltsum', False),
                       scratch=config_dict.get('scratch', None),
                       dry_run=dry_run)

        self._set_link('residual-cr', ResidualCR_SG,
                       comp=comp, data=data,
                       mktimefilter=config_dict.get('mktimefitler', None),
                       hpx_order=config_dict.get('hpx_order_fitting', 4),
                       clean=config_dict.get('clean_class', None),
                       dirty=config_dict.get('dirty_class', None),                       
                       select_factor=config_dict.get('select_factor', None),
                       mask_factor=config_dict.get('mask_factor', None),
                       sigma=config_dict.get('sigma', None),
                       full_output=config_dict.get('full_output', False),
                       dry_run=dry_run)



def register_residual_cr():
    """Register these classes with the `LinkFactory` """
    ResidualCR.register_class()
    ResidualCR_SG.register_class()
    ResidualCRChain.register_class()
