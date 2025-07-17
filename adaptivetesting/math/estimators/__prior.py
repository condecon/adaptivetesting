import numpy as np
from abc import ABC, abstractmethod
from scipy.stats import norm, rv_continuous


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


class CustomPrior(Prior):
    def __init__(self,
                 random_variable: rv_continuous,
                 *args: float,
                 loc: float = 0,
                 scale: float = 1):
        """This class is for using a custom prior in the ability estimation
        in Bayes Modal or Expected a Posteriori.
        Any continous, univariate random variable from the scipy.stats module can be used.
        However, you have to consult to the scipy documentation for the required parameters for
        the probability density function (pdf) of that particular random variable.

        Args:
            random_variable (rv_continuous): Any continous, univariate random variable from the scipy.stats module.
            
            *args (float): Custom parameters required to calculate the pdf of that specific random variable.

            loc (float, optional): Location parameter. Defaults to 0.
            
            scale (float, optional): Scale parameter. Defaults to 1.
        """
        super().__init__()
        self.random_variable = random_variable
        self.args = args
        self.loc = loc
        self.scale = scale
    
    def pdf(self, x: float | np.ndarray) -> np.ndarray:
        result = self.random_variable.pdf(
            x,
            *self.args,
            self.loc,
            self.scale
        )
        return np.array(result)


class CustomPriorException(Exception):
    """This exception can be used is the custom prior
    is not correctly specified.

    It is usually raised if a non-normal prior is used
    that was not correctly inherited from the `CustomPrior` class.
    """
    pass
