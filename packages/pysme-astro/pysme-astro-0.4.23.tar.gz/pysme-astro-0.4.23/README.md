![Python application](https://github.com/AWehrhahn/SME/workflows/Python%20application/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/pysme-astro/badge/?version=latest)](https://pysme-astro.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/150097199.svg)](https://zenodo.org/badge/latestdoi/150097199)



# PySME

Spectroscopy Made Easy (SME) is a software tool that fits an observed
spectrum of a star with a model spectrum. Since its initial release in
[1996](http://adsabs.harvard.edu/abs/1996A%26AS..118..595V), SME has been a
suite of IDL routines that call a dynamically linked library, which is
compiled from C++ and fortran. This classic IDL version of SME is available
for [download](http://www.stsci.edu/~valenti/sme.html).

In 2018, we began began reimplmenting the IDL part of SME in python 3,
adopting an object oriented paradigm and continuous itegration practices
(code repository, build automation, self-testing, frequent builds).

# Installation

A stable version is available on pip `pip install pysme-astro`
If you are interested in the latest version you can do so by cloning this git.
```bash
# Clone the git repository
git clone https://github.com/AWehrhahn/SME.git
# Move to the new directory
cd SME
# Install this folder (as an editable module)
pip install -e .
```
See also the [documentation](https://pysme-astro.readthedocs.io/en/latest/usage/installation.html)

# Poster

A poster about PySME can be found here: [Poster](http://sme.astro.uu.se/poster.html)

# GUI

A GUI for PySME is available in its own repository [PySME-GUI](https://github.com/AWehrhahn/PySME-GUI).
