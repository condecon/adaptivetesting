from abc import ABC, abstractmethod


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
    