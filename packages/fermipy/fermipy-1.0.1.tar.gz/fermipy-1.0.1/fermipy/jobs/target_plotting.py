#!/usr/bin/env python
#

# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Module with classes for plotting and SED and to  
paralleize that analysis.
"""
from __future__ import absolute_import, division, print_function

from os.path import splitext

from astropy.io import fits

from fermipy.utils import init_matplotlib_backend, load_yaml

from fermipy.jobs.link import Link
from fermipy.jobs.scatter_gather import ScatterGather
from fermipy.jobs.slac_impl import make_nfs_path

from fermipy.castro import CastroData
from fermipy.sed_plotting import plotCastro, plotBands,\
    plotSED_OnAxis, plotSED


from fermipy.jobs.name_policy import NameFactory
from fermipy.jobs import defaults

init_matplotlib_backend()
NAME_FACTORY = NameFactory(basedir='.')


class PlotCastro(Link):
    """Small class to plot an SED as a 'Castro' plot.
    """
    appname = 'fermipy-plot-castro'
    linkname_default = 'plot-castro'
    usage = '%s [options]' % (appname)
    description = "Plot likelihood v. flux normalization and energy"

    default_options = dict(infile=defaults.generic['infile'],
                           outfile=defaults.generic['outfile'])

    __doc__ += Link.construct_docstring(default_options)

    def run_analysis(self, argv):
        """Run this analysis"""
        args = self._parser.parse_args(argv)

        exttype = splitext(args.infile)[-1]
        if exttype in ['.fits', '.npy']:
            castro_data = CastroData.create_from_sedfile(args.infile)
        elif exttype in ['.yaml']:
            castro_data = CastroData.create_from_yamlfile(args.infile)
        else:
            raise ValueError("Can not read file type %s for SED" % extype)

        ylims = [1e-8, 1e-5]

        plot = plotCastro(castro_data, ylims, nstep=100)
        if args.outfile:
            plot[0].savefig(args.outfile)



class PlotCastro_SG(ScatterGather):
    """Small class to generate configurations for the `PlotCastro` class.

    This loops over all the targets defined in the target list.
    """
    appname = 'fermipy-plot-castro-sg'
    usage = "%s [options]" % (appname)
    description = "Make castro plots for set of targets"
    clientclass = PlotCastro

    job_time = 60

    default_options = dict(ttype=defaults.common['ttype'],
                           targetlist=defaults.common['targetlist'])

    __doc__ += Link.construct_docstring(default_options)

    def build_job_configs(self, args):
        """Hook to build job configurations
        """
        job_configs = {}

        ttype = args['ttype']
        (targets_yaml, sim) = NAME_FACTORY.resolve_targetfile(args)
        if targets_yaml is None:
            return job_configs

        targets = load_yaml(targets_yaml)

        for target_name, target_list in targets.items():
            for targ_prof in target_list:
                name_keys = dict(target_type=ttype,
                                 target_name=target_name,
                                 profile=targ_prof,
                                 fullpath=True)
                targ_key = "%s_%s" % (target_name, targ_prof)
                input_path = NAME_FACTORY.sedfile(**name_keys)
                output_path = input_path.replace('.fits', '.png')
                logfile = make_nfs_path(input_path.replace('.fits', '.log'))
                job_config = dict(infile=input_path,
                                  outfile=output_path,
                                  logfile=logfile)
                job_configs[targ_key] = job_config

        return job_configs



class PlotSEDSummaryBands(Link):
    """Small class to plot an SED as a 'Castro' plot.
    """
    appname = 'fermipy-plot-sed-summary-bands'
    linkname_default = 'plot-sed-summary-bands'
    usage = '%s [options]' % (appname)
    description = "Plot SED limits"

    default_options = dict(infile=defaults.generic['infile'],
                           outfile=defaults.generic['outfile'],
                           summaryfile=defaults.generic['summaryfile'],
                           band_type=defaults.sims['band_type'])


    __doc__ += Link.construct_docstring(default_options)

    def run_analysis(self, argv):
        """Run this analysis"""
        args = self._parser.parse_args(argv)

        exttype = splitext(args.infile)[-1]
        if exttype in ['.fits', '.npy']:
            castro_data = CastroData.create_from_sedfile(args.infile)
        elif exttype in ['.yaml']:
            castro_data = CastroData.create_from_yamlfile(args.infile)
        else:
            raise ValueError("Can not read file type %s for SED" % extype)

        ylims = [1e-8, 1e-5]

        if args.summaryfile is not None:
            bands = fits.open(args.summaryfile)
            fig, ax = plotBands(castro_data, ylims, bands[1], band_type=args.band_type)
            plotSED_OnAxis(ax, castro_data)
        else:
            fig, ax = plotSED_OnAxis(ax, ylims)

        if args.outfile:
            fig.savefig(args.outfile)



class PlotSEDSummaryBands_SG(ScatterGather):
    """Small class to generate configurations for the `PlotSEDLimits` class.

    This loops over all the targets defined in the target list.
    """
    appname = 'fermipy-plot-sed-summary-bands-sg'
    usage = "%s [options]" % (appname)
    description = "Make sed plots for set of targets"
    clientclass = PlotSEDSummaryBands

    job_time = 60

    default_options = dict(ttype=defaults.common['ttype'],
                           targetlist=defaults.common['targetlist'],
                           nsims=defaults.sims['nsims'],
                           seed=defaults.sims['seed'],
                           band_sim=defaults.sims['band_sim'],
                           band_type=defaults.sims['band_type'])

    __doc__ += Link.construct_docstring(default_options)

    def build_job_configs(self, args):
        """Hook to build job configurations
        """
        job_configs = {}

        ttype = args['ttype']
        (targets_yaml, sim) = NAME_FACTORY.resolve_targetfile(args)
        if targets_yaml is None:
            return job_configs

        targets = load_yaml(targets_yaml)
        first = args['seed']
        last = first + args['nsims'] - 1

        for target_name, target_list in targets.items():
            for targ_prof in target_list:
                name_keys = dict(target_type=ttype,
                                 target_name=target_name,
                                 profile=targ_prof,
                                 fullpath=True)
                targ_key = "%s_%s" % (target_name, targ_prof)
                input_path = NAME_FACTORY.sedfile(**name_keys)
                output_path = input_path.replace('.fits', '.png')
                logfile = make_nfs_path(input_path.replace('.fits', '.log'))
                sed_file = NAME_FACTORY.sim_sedfile(sim_name=args['band_sim'],
                                                    **name_keys)
                summaryfile = sed_file.replace('_SEED.fits',
                                               '_summary_%06i_%06i.fits' % (first, last))

                job_config = dict(infile=input_path,
                                  outfile=output_path,
                                  summaryfile=summaryfile,
                                  band_sim=args['band_sim'],
                                  logfile=logfile)
                                  
                job_configs[targ_key] = job_config

        return job_configs


def register_classes():
    """Register these classes with the `LinkFactory` """
    PlotCastro.register_class()
    PlotCastro_SG.register_class()
    PlotSEDSummaryBands.register_class()
    PlotSEDSummaryBands_SG.register_class()
