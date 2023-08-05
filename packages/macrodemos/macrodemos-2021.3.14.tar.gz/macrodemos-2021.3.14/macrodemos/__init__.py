"""
macrodemos : A Python module to teach macroeconomics and macroeconometrics

This package contains Dash apps to teach and learn about macroeconomics and macroeconometrics.

So far, the available demos are:

    ARMA_demo():  to study AutoRegressive Moving Average processes.
    filters_demo(): to compare several filtering methods.
    Markov_demo(): to study Markov chains.
    Solow_demo():  to study the Solow growth model.

Randall Romero Aguilar, 2016-2021
"""

#import .constants
#import .common_components
from .captura import read_IFS
from .demo_ARMA import ARMA_demo
from .demo_Solow import Solow_demo
from .demo_Markov import Markov_demo
from .demo_filters import filters_demo

