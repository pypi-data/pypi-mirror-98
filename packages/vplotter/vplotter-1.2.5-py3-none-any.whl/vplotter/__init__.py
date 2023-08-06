# -*- coding: utf-8 -*-
from .vplotter import Plotter

from setuptools import setup, find_packages

__all__ = (
    '__version__',
    'Plotter'
)

import pkg_resources
__version__           = pkg_resources.get_distribution("vplotter").version

__short_description__ = "Plotter class for any purpose, based on Veusz."
__license__           = "MIT"
__author__            = "Alexander D. Kazakov | Varvara M. Prokacheva"
__author_email__      = "alexander.d.kazakov@gmail.com"
__github_username__   = "AlexanderDKazakov"
