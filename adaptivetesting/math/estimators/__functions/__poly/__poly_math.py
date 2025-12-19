from abc import ABC, abstractmethod
from scipy.optimize import minimize_scalar, OptimizeResult
from .....models.__algorithm_exception import AlgorithmException
from .....models.__test_item import PolyItem
import numpy as np


class PolyModelFunctions(ABC):
    
    @abstractmethod
    @staticmethod
    def category_prob(theta: float,
                      a: float,
                      thresholds_list: list[float],
                      response_pattern: int):
        pass

    @abstractmethod
    @staticmethod
    def log_likelihood(theta: float,
                       a_params: list[float],
                       thresholds_list: list[list[float]],
                       response_pattern: list[int]):
        pass
    
    @abstractmethod
    @staticmethod
    def fisher_information(theta: float,
                           a: float,
                           thresholds: list[float],
                           response: int):
        pass
    
    def maximize_likelihood_function(self,
                                     a_params: list[float],
                                     thresholds_list: list[list[float]],
                                     response_pattern: list[int],
                                     border: tuple[float, float] = (-10, 10)):

        result: OptimizeResult = minimize_scalar(lambda mu: -self.log_likelihood(mu, a_params, thresholds_list, response_pattern),
                                                bounds=border,
                                                method='bounded') # type: ignore

        if not result.success:
            raise AlgorithmException(f"Optimization failed: {result.message}")
        else:
            return result.x