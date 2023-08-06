
import numpy as np
import pyIrfLoader

pyIrfLoader.Loader_go()

evtype_string = {
    1: 'FRONT',
    2: 'BACK',
    4: 'PSF0',
    8: 'PSF1',
    16: 'PSF2',
    32: 'PSF3',
    64: 'EDISP0',
    128: 'EDISP1',
    256: 'EDISP2',
    512: 'EDISP3',
}




def create_irf(event_class, event_type):
    if isinstance(event_type, int):
        event_type = evtype_string[event_type]

    irf_factory = pyIrfLoader.IrfsFactory.instance()
    irfname = '%s::%s' % (event_class, event_type)
    irf = irf_factory.create(irfname)
    return irf


def create_psf(event_class, event_type, dtheta, egy, cth):
    """Create an array of PSF response values versus energy and
    inclination angle.

    Parameters
    ----------
    egy : `~numpy.ndarray`
        Energy in MeV.

    cth : `~numpy.ndarray`
        Cosine of the incidence angle.

    """
    irf = create_irf(event_class, event_type)
    theta = np.degrees(np.arccos(cth))
    m = np.zeros((len(dtheta), len(egy), len(cth)))

    for i, x in enumerate(egy):
        for j, y in enumerate(theta):
            m[:, i, j] = irf.psf().value(dtheta, x, y, 0.0)

    return m

def bitmask_to_bits(mask):

    bits = []
    for i in range(32):
        if mask & (2**i):
            bits += [2**i]

    return bits





def create(event_class, event_types, energies, cth_bins=None, ndtheta=500, nbin=64):
    """Create a PSFModel object.  This class can be used to evaluate the
    exposure-weighted PSF for a source with a given observing
    profile and energy distribution.
    
    Parameters
    ----------
    skydir : `~astropy.coordinates.SkyCoord`

    ltc : `~fermipy.irfs.LTCube`

    energies : `~numpy.ndarray`
        Grid of energies at which the PSF will be pre-computed.

    cth_bins : `~numpy.ndarray`
        Bin edges in cosine of the inclination angle.
            
    use_edisp : bool
        Generate the PSF model accounting for the influence of
        energy dispersion.

    fn : `~fermipy.spectrum.SpectralFunction`
        Model for the spectral energy distribution of the source.

    """

    if isinstance(event_types, int):
        event_types = bitmask_to_bits(event_types)

    dtheta = np.logspace(-4, 1.75, ndtheta)
    dtheta = np.insert(dtheta, 0, [0])
 
    if cth_bins is None:
        cth_bins = np.array([0.2, 1.0])

    for ev_type in event_types:
        psf = create_psf(event_class, ev_type, dtheta, energies, cth_bins)


if __name__ == "__main__":
    irfs = 'P8R3_SOURCE_V2'
    evtype = 3
    energies = np.logspace(2,5,13)
    
    create(irfs, evtype, energies)
