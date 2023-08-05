from os.path import dirname

import pytest
import numpy as np

from pysme.sme import SME_Structure as SME_Struct
from pysme.abund import Abund
from pysme.atmosphere.krzfile import KrzFile
from pysme.linelist.linelist import LineList
from pysme.sme_synth import SME_DLL
from pysme.nlte import nlte

# Create Objects to pass to library
# Their functionality is tested in other test files, so we assume it works
@pytest.fixture
def cwd():
    return dirname(__file__)


@pytest.fixture
def libsme():
    return SME_DLL()


@pytest.fixture
def teff():
    return 5000


@pytest.fixture
def grav():
    return 4.2


@pytest.fixture
def vturb():
    return 0.1


@pytest.fixture
def wfirst():
    return 5500


@pytest.fixture
def wlast():
    return 5600


@pytest.fixture
def vw_scale():
    return 2.5


@pytest.fixture
def mu():
    return [1]


@pytest.fixture
def accrt():
    return 0.1


@pytest.fixture
def accwt():
    return 0.1


@pytest.fixture
def linelist():
    linelist = LineList()
    linelist.add("Fe 1", 5502.9931, 0.9582, -3.047, 7.19, -6.22, 239.249)
    linelist.add("Cr 2", 5503.5955, 4.1682, -2.117, 8.37, -6.49, 195.248)
    linelist.add("Mn 1", 5504.0000, 2.0000, -3.000, 8.00, -6.50, 200.247)
    return linelist


@pytest.fixture
def atmo(cwd):
    return KrzFile(cwd + "/testatmo1.krz")


@pytest.fixture
def abund():
    return Abund(monh=0, pattern="Asplund2009")


def test_basic(libsme, wfirst, wlast, vw_scale):
    """ Test instantiation of library object and some basic functions """
    print(libsme.SMELibraryVersion())
    libsme.InputWaveRange(wfirst, wlast)
    libsme.SetVWscale(vw_scale)
    libsme.SetH2broad()

    print(libsme.file, libsme.wfirst, libsme.wlast, libsme.vw_scale, libsme.h2broad)

    # assert libsme.file
    assert libsme.wfirst == wfirst
    assert libsme.wlast == wlast
    assert libsme.vw_scale == vw_scale
    assert libsme.h2broad


def test_linelist(libsme, linelist):
    """ Test linelist behaviour """
    libsme.InputLineList(linelist)
    outlist = libsme.OutputLineList()

    print(libsme.linelist)
    fmt = "  Out: {0:10.4f},{2:7.4f},{1:7.3f},{3:5.2f},{4:6.2f},{5:8.3f}"
    for i in range(len(linelist)):
        outline = [x for x in outlist[i]]
        outline[1] = np.log10(outline[1])
        print(fmt.format(*outline))

    # TODO
    # libsme.UpdateLineList()

    with pytest.raises(TypeError):
        libsme.InputLineList(None)


def test_atmosphere(libsme, atmo, teff, grav, vturb):
    """ Test atmosphere behaviour """

    libsme.InputModel(teff, grav, vturb, atmo)

    # TODO test different geometries

    assert libsme.teff == teff
    assert libsme.grav == grav
    assert libsme.vturb == vturb
    assert libsme.ndepth == len(atmo[atmo.depth])

    with pytest.raises(ValueError):
        libsme.InputModel(-1000, grav, vturb, atmo)

    with pytest.raises(ValueError):
        libsme.InputModel(teff, grav, -10, atmo)

    with pytest.raises(TypeError):
        libsme.InputModel(teff, grav, vturb, None)


def test_abund(libsme, abund):
    """ Test abundance behaviour """
    libsme.InputAbund(abund)

    # TODO: What should be the expected behaviour?
    empty = Abund(monh=0, pattern="empty")
    empty.update_pattern({"H": 12})
    libsme.InputAbund(empty)

    with pytest.raises(TypeError):
        libsme.InputAbund(None)


def test_transf(
    libsme,
    linelist,
    teff,
    grav,
    vturb,
    atmo,
    abund,
    vw_scale,
    wfirst,
    wlast,
    mu,
    accrt,
    accwt,
):
    """ Test radiative transfer """
    libsme.SetLibraryPath()

    libsme.InputLineList(linelist)
    libsme.InputModel(teff, grav, vturb, atmo)
    libsme.InputAbund(abund)
    libsme.Ionization(0)
    libsme.SetVWscale(vw_scale)
    libsme.SetH2broad()

    libsme.InputWaveRange(wfirst, wlast)
    libsme.Opacity()

    nw, wave, synth, cont = libsme.Transf(mu, accrt, accwt)

    print(nw, wave, synth, cont)
    assert nw == 47

    density = libsme.GetDensity()
    print(atmo.rho)
    print(density)
    assert np.allclose(density, atmo.rho, rtol=1e-1, equal_nan=True)

    xne = libsme.GetNelec()
    print(xne)
    print(atmo.xne)
    assert np.allclose(xne, atmo.xne, rtol=2e-1)

    xna = libsme.GetNatom()
    print(xne)
    print(atmo.xne)
    assert np.allclose(xna, atmo.xna, rtol=1e-1)

    libsme.GetLineOpacity(linelist.wlcent[0])
    libsme.GetLineRange()
    for switch in range(-3, 13):
        if switch != 8:
            libsme.GetOpacity(switch)
