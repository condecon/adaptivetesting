from enum import Enum


class ResultOutputFormat(Enum):
    """
    Enum for selecting the output format for
    the test results
    """
    CSV = 1
    PICKLE = 2


class StoppingCriterion(Enum):
    """Enum for selecting the stopping criterion
    for the adaptive test"""
    SE = 1
    LENGTH = 2
