# TODO implement NLTE tests

import pytest

import os
from os.path import dirname
import tempfile

import numpy as np

from pysme.sme import SME_Structure as SME_Struct
from pysme.iliffe_vector import Iliffe_vector
from pysme.linelist.vald import ValdFile
from pysme.sme_synth import SME_DLL
from pysme.nlte import nlte, DirectAccessFile
from pysme.synthesize import Synthesizer, synthesize_spectrum
from pysme.config import Config
from pysme.abund import Abund

from .test_largefilestorage import skipif_lfs, lfs_nlte, lfs_atmo

cwd = dirname(__file__)


def make_minimum_structure():
    sme = SME_Struct()
    sme.teff = 5000
    sme.logg = 4.4
    sme.vmic = 1
    sme.vmac = 1
    sme.vsini = 1
    sme.abund = Abund.solar()
    sme.linelist = ValdFile("{}/testcase3.lin".format((cwd)))
    sme.atmo.source = "marcs2012p_t2.0.sav"
    sme.atmo.method = "grid"

    sme.wran = [[6436, 6444]]

    return sme


def test_activate_nlte():
    sme = make_minimum_structure()

    # Make sure nothing is set yet
    assert len(sme.nlte.elements) == 0

    # Add an element
    sme.nlte.set_nlte("Ca", "marcs2012p_t1.0_Ca.grd")
    assert len(sme.nlte.elements) == 1
    assert "Ca" in sme.nlte.elements

    # Add it again, shouldn't change anything
    sme.nlte.set_nlte("Ca", "marcs2012p_t1.0_Ca.grd")
    assert len(sme.nlte.elements) == 1
    assert "Ca" in sme.nlte.elements

    # Try to remove something else
    sme.nlte.remove_nlte("Na")
    assert len(sme.nlte.elements) == 1
    assert "Ca" in sme.nlte.elements

    # Remove the original element
    sme.nlte.remove_nlte("Ca")
    assert len(sme.nlte.elements) == 0

    # Add a element with a custom grid
    sme.nlte.set_nlte("Na", "test_grid.grd")
    assert len(sme.nlte.elements) == 1
    assert "Na" in sme.nlte.elements
    assert sme.nlte.grids["Na"] == "test_grid.grd"

    # Update custom grid
    sme.nlte.set_nlte("Na", "test_grid2.grd")
    assert len(sme.nlte.elements) == 1
    assert sme.nlte.grids["Na"] == "test_grid2.grd"

    # Add element without default grid
    with pytest.raises(ValueError):
        sme.nlte.set_nlte("U")

    # with a grid it should work
    sme.nlte.set_nlte("U", "test_grid.grd")
    assert sme.nlte.grids["U"] == "test_grid.grd"


@skipif_lfs
def test_run_with_nlte():
    # NOTE sme structure must have long format for NLTE
    sme = make_minimum_structure()
    sme.nlte.set_nlte("Ca", "marcs2012p_t1.0_Ca.grd")

    sme2 = synthesize_spectrum(sme)

    assert isinstance(sme2.nlte.flags, np.ndarray)
    assert np.issubdtype(sme2.nlte.flags.dtype, np.dtype("bool"))
    assert len(sme2.nlte.flags) == len(sme2.linelist)
    assert np.any(sme2.nlte.flags)


@skipif_lfs
@pytest.mark.usefixtures("lfs_atmo", "lfs_nlte")
def test_dll(lfs_atmo, lfs_nlte):
    sme = make_minimum_structure()
    elem = "Ca"
    sme.nlte.set_nlte(elem, "marcs2012p_t1.0_Ca.grd")

    libsme = SME_DLL()
    libsme.ResetNLTE()

    syn = Synthesizer(None, lfs_atmo=lfs_atmo, lfs_nlte=lfs_nlte)
    sme = syn.get_atmosphere(sme)
    libsme.InputLineList(sme.linelist)
    libsme.InputModel(sme.teff, sme.logg, sme.vmic, sme.atmo)

    # This is essentially what update_depcoefs does, just for one element
    counter = 0
    bmat, linerefs, lineindices = nlte(sme, libsme, elem, lfs_nlte)
    for lr, li in zip(linerefs, lineindices):
        if lr[0] != -1 and lr[1] != -1:
            counter += 1
            libsme.InputNLTE(bmat[:, lr], li)

    flags = libsme.GetNLTEflags()
    assert np.any(flags)
    assert np.count_nonzero(flags) == counter
    assert len(flags) == len(sme.linelist)

    idx = np.where(flags)[0][0]
    coeffs = libsme.GetNLTE(idx)
    assert coeffs is not None

    # If we reset NLTE no flags should be set
    libsme.ResetNLTE()
    flags = libsme.GetNLTEflags()
    assert not np.any(flags)
    assert len(flags) == len(sme.linelist)

    with pytest.raises(TypeError):
        libsme.InputNLTE(None, 0)

    with pytest.raises(TypeError):
        libsme.InputNLTE(bmat[:, [0, 1]], 0.1)

    with pytest.raises(ValueError):
        libsme.InputNLTE([0, 1], 10)

    with pytest.raises(ValueError):
        libsme.InputNLTE(bmat[:, [0, 1]], -10)


@pytest.fixture
def temp():
    file = tempfile.NamedTemporaryFile(delete=False)
    yield file.name
    try:
        os.remove(file)
    except:
        pass


def test_read_write_direct_access_file(temp: str):
    content = {
        "hello": "world",
        "I": ["have", "the", "high", "ground"],
        "teff": np.arange(100),
    }

    DirectAccessFile.write(temp, **content)
    daf = DirectAccessFile(temp)

    for key, value in content.items():
        vf = daf[key]
        if np.issubdtype(vf.dtype, np.dtype("S")):
            vf = np.char.decode(vf)

        assert np.all(vf == value)
