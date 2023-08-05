Power Spectra Generation pipeline for CD/EoR experiments
========================================================

pspipe is an analysis pipeline which aims to make generation of high precision power-spectra for Cosmic Dawn and Epoch of Reionization experiments as easy and reproducible as possible. pspipe is the default analysis pipeline of the [Lofar-EoR](http://www.lofar.org/astronomy/eor-ksp/epoch-reionization.html) and [NenuFAR](https://nenufar.obs-nancay.fr/en/homepage-en/) CD projects. It performs all tasks from calibrated data to final the power-spectra, including:

- Post-calibration flagging (using [AOflagger](https://sourceforge.net/p/aoflagger/wiki/Home/) and [SSINS](https://arxiv.org/abs/1906.01093))
- Visibility gridding (using [WSClean](https://sourceforge.net/p/wsclean/wiki/Home/))
- Foregrounds modeling and removal (using [GPR](https://doi.org/10.1093/mnras/sty1207), [GMCA](https://arxiv.org/abs/1209.4769), polynomial fitting)
- Optimal power-spectra generation (using [ps_eor](https://gitlab.com/flomertens/ps_eor))

Thanks to its multi-nodes concurrent processing, pspipe is also very fast at crunching hundreds of hour of calibrated data.

Installation
------------

pspipe can be installed via pip:

    $ pip install pspipe

and requires Python 3.7.0 or higher. For certain tasks, you will also need [DPPP](https://github.com/lofar-astron/DP3/tree/master/DPPP) and [WSClean](https://sourceforge.net/p/wsclean/wiki/Home/)

Documentation
--------------

Please check the [wiki page](https://gitlab.com/flomertens/pspipe/-/wikis/home).
