"""
spotdesirability - a Python package for desirability function analysis.

This package provides tools for multi-objective optimization using
desirability functions, including various desirability classes,
test functions, and visualization utilities.

Version: 0.0.13
License: GPL-2.0
"""

from spotdesirability.utils.desirability import (
    DesirabilityBase,
    DMax,
    DMin,
    DTarget,
    DArb,
    DBox,
    DCategorical,
    DOverall,
)
from spotdesirability.functions.rsm import conversion_pred, activity_pred, rsm_opt
from spotdesirability.plot.ccd import plotCCD

__version__ = "0.0.13"

__all__ = [
    # Desirability classes
    "DesirabilityBase",
    "DMax",
    "DMin",
    "DTarget",
    "DArb",
    "DBox",
    "DCategorical",
    "DOverall",
    # RSM functions
    "conversion_pred",
    "activity_pred",
    "rsm_opt",
    # Plotting
    "plotCCD",
]
