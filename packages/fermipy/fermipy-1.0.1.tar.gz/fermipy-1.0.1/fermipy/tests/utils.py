# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function
import os
import re
from astropy.tests.helper import pytest
from fermipy import get_st_version, get_git_version, get_git_version_fp

__all__ = ['requires_dependency', 'requires_st_version', 'requires_git_version', 'requires_file', 'create_diffuse_dir']


def requires_file(filepath):

    skip_it = True if not os.path.isfile(filepath) else False
    return pytest.mark.skipif(skip_it,
                              reason='File %s does not exist.' % filepath)


def version_str_to_int(version_str):

    m = re.search('(\d\d)-(\d\d)-(\d\d)', version_str)
    if m is None:
        m = re.search('(\d*)\.(\d*)\.(\d*).*', version_str)
    if m is None:
        return 0
    else:
        return (int(m.group(1)) * 10000 +
                int(m.group(2)) * 100 + int(m.group(3)))

def version_str_to_int_git(version_str):

    m = re.search('Fermitools.(\d*)\.(\d*)\.(\d*).*', version_str)

    if m is None:
        return 0
    else:
        return (int(m.group(1)) * 10000 +
                int(m.group(2)) * 100 + int(m.group(3)))


def requires_st_version(version_str):
    """Decorator to declare minimum ST version needed for tests.
    """
    reason = 'Requires ST Version >=: {}'.format(version_str)

    version = version_str_to_int(version_str)

    st_version = get_st_version()
    if st_version == 'unknown':
        return pytest.mark.skipif(False, reason=reason)
    
    try:
        st_version = version_str_to_int(get_st_version())
    except:
        st_version = 0

    if st_version >= version:
        skip_it = False
    else:
        skip_it = True

    return pytest.mark.skipif(skip_it, reason=reason)


def requires_git_version(version_str):
    """Decorator to declare minimum ST version needed for tests.
    """

    version = version_str_to_int(version_str)
    try:
        st_version = version_str_to_int_git(get_git_version_fp())
    except:
        st_version = 0

    if st_version >= version:
        skip_it = False
    else:
        skip_it = True

    reason = 'Requires ST Version >=: {}'.format(version_str)
    return pytest.mark.skipif(skip_it, reason=reason)


def requires_dependency(name):
    """Decorator to declare required dependencies for tests.

    Examples
    --------

    ::

        from fermipy.tests.utils import requires_dependency

        @requires_dependency('scipy')
        def test_using_scipy():
            import scipy
            ...

        @requires_dependency('Fermi ST')
        def test_using_fermi_science_tools():
            import pyLikelihood
            ...
    """
    if name == 'Fermi ST':
        name = 'pyLikelihood'

    try:
        __import__(name)
        skip_it = False
    except ImportError:
        skip_it = True

    reason = 'Missing dependency: {}'.format(name)
    return pytest.mark.skipif(skip_it, reason=reason)



@pytest.fixture(scope='package')
def create_diffuse_dir(request, tmpdir_factory):
    path = tmpdir_factory.mktemp('diffuse')
    url = 'https://raw.githubusercontent.com/fermiPy/fermipy-extras/master/data/diffuse.tar.gz'
    outfile = path.join('diffuse.tar.gz')
    dirname = path.join()
    os.system('curl -o %s -OL %s' % (outfile, url))
    os.system('cd %s;tar xzf %s' % (dirname, outfile))
    
    request.addfinalizer(lambda: path.remove(rec=1))

    gll_file = path.join('diffuse', 'gll_iem_v07.fits')
    if not os.path.isfile(str(gll_file)):
        raise RuntimeError("Failed to install diffuse file %s" % str(gll_file))
    os.environ['FERMI_DIFFUSE_DIR'] = os.path.abspath(os.path.dirname(gll_file))
    
