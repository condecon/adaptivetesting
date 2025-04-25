import jax.numpy as np
from abc import ABC, abstractmethod
from scipy.stats import norm


class Prior(ABC):
    def __init__(self):
        """Base class for prior distributions
        """
        pass

    @abstractmethod
    def pdf(self, x: float | np.ndarray) -> np.ndarray:
        """Probability density function for a prior distribution

        Args:
            x (float | np.ndarray): point at which to calculate the function value
        
        Returns:
            ndarray: function value
        """
        pass


class NormalPrior(Prior):
    def __init__(self, mean: float, sd: float):
        """Normal distribution as prior for Bayes Modal estimation

        Args:
            mean (float): mean of the distribution
            
            sd (float): standard deviation of the distribution
        """
        self.mean = mean
        self.sd = sd
        super().__init__()

    def pdf(self, x: float | np.ndarray) -> np.ndarray:
        """Probability density function for a prior distribution

        Args:
            x (float | np.ndarray): point at which to calculate the function value
        
        Returns:
            ndarray: function value
        """
        return norm.pdf(x, self.mean, self.sd) # type: ignore
