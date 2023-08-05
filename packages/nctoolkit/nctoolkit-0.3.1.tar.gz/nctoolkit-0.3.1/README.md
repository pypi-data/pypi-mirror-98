
<!-- README.md is generated from README.Rmd. Please edit that file -->

[![pypi](https://img.shields.io/pypi/v/nctoolkit.svg)](https://pypi.python.org/pypi/nctoolkit/)
[![Conda Latest Release](https://anaconda.org/conda-forge/nctoolkit/badges/version.svg)](https://anaconda.org/conda-forge/nctoolkit/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/pmlmodelling/nctoolkit/issues) 
[![codecov](https://codecov.io/gh/pmlmodelling/nctoolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/pmlmodelling/nctoolkit)
[![Build Status](https://travis-ci.org/pmlmodelling/nctoolkit.png?branch=master)](https://travis-ci.org/pmlmodelling/nctoolkit)
[![Documentation Status](https://readthedocs.org/projects/nctoolkit/badge/?version=latest)](https://nctoolkit.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4494237.svg)](https://doi.org/10.5281/zenodo.4494237)






# nctoolkit - Fast and easy analysis of netCDF data in Python 

nctoolkit is a comprehensive Python (3.6 and above) package for analyzing netCDF data on Linux and macOS.

Core abilities include:
   - Clipping to spatial regions
   - Calculating climatologies
   - Subsetting to specific time periods
   - Calculating spatial statistics
   - Creating new variables using arithmetic operations
   - Calculating anomalies
   - Calculating rolling and cumulative statistics
   - Horizontally and vertically remapping data
   - Calculating time averages
   - Interactive plotting of data
   - Calculating the correlations between variables
   - Calculating vertical statistics for the likes of oceanic data
   - Calculating ensemble statistics
   - Calculating phenological metrics

## Installation

The easiest way to install the package is using conda. This will install nctoolkit and all system dependencies.
```sh
conda install -c conda-forge nctoolkit
```

Install through [PyPI](https://pypi.org/project/nctoolkit/) using pip:
```sh
pip install nctoolkit 
```

Install the development version using using pip:
```sh
pip install --force-reinstall git+https://github.com/pmlmodelling/nctoolkit.git
```

This package requires the installation of [Climate Data Operators](https://code.mpimet.mpg.de/projects/cdo/wiki). The conda installation will handle this for you. Otherwise, you will have to install it.  The easiest way is using conda:

```sh
conda install -c conda-forge cdo 
```

A couple of methods give users the option of using [NetCDF Operators](http://nco.sourceforge.net/) instead of CDO as the computational backend. Again, the easiest way to install is using conda:

```sh
conda install -c conda-forge nco 
```

If you want to install CDO from source, bash scripts are available [here](https://github.com/pmlmodelling/nctoolkit/tree/master/cdo_installers).
 
nctoolkit is tested with continuous integration using Travis (for Linux) and GitHub actions (for Mac OS). It will not work on Windows platforms today or in future, because of system dependency limitations. 



## Fixing plotting problem due to xarray bug

There is currently a bug in xarray caused by the update of pandas to version 1.1. As a result some plots will fail in nctoolkit. To fix this ensure pandas version 1.0.5 is installed. Do this after installing nctoolkit. This can be done as follows:


```sh
conda install -c conda-forge pandas=1.0.5 
```

or

```sh
pip install pandas==1.0.5
```














## Reference and tutorials

A full API reference, in depth tutorials and a how-to guide are available at [readthedocs](https://nctoolkit.readthedocs.io/en/latest/).






















