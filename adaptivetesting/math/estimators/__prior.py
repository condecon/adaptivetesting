import numpy as np
from abc import ABC, abstractmethod
from scipy.stats import norm, skewnorm, rv_continuous, gaussian_kde


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
        """Normal distribution as prior for Bayes Modal or EAP estimation

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
    
    def logpdf(self, x: float | np.ndarray):
        return norm.logpdf(x, self.mean, self.sd)
    

class SkewNormalPrior(Prior):
    def __init__(self, skewness: float, loc: float, scale: float):
        """Skew normal distribution as prior for Bayes Modal or EAP estimation

            Args:
                loc (float): location parameter
                
                scale (float): scale parameter
        """
        super().__init__()
        self.skewness = skewness
        self.loc = loc
        self.scale = scale

    def pdf(self, x):
        """Probability density function for a prior distribution

        Args:
            x (float | np.ndarray): point at which to calculate the function value
        
        Returns:
            ndarray: function value
        """
        return skewnorm.pdf(x,
                            self.skewness,
                            loc=self.loc,
                            scale=self.scale)
    
    def logpdf(self, x: float | np.ndarray):
        return skewnorm.logpdf(x, self.skewness,
                               loc=self.loc,
                               scale=self.scale)


class CustomPrior(Prior):
    def __init__(self,
                 random_variable: rv_continuous,
                 *args: float,
                 loc: float = 0,
                 scale: float = 1):
        """This class is for using a custom prior in the ability estimation
        in Bayes Modal or Expected a Posteriori.
        Any continuous, univariate random variable from the scipy.stats module can be used.
        However, you have to consult to the scipy documentation for the required parameters for
        the probability density function (pdf) of that particular random variable.

        Args:
            random_variable (rv_continuous): Any continuous, univariate random variable from the scipy.stats module.
            
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


class EmpiricalPrior(Prior):
    """
    A prior distribution constructed from empirical samples using a kernel density estimate (KDE).
    This class wraps scipy.stats.gaussian_kde to provide a nonparametric prior estimated
    from observed data. The KDE is built from the provided dataset at initialization and
    used to evaluate the probability density (pdf) at query points.
    
    
    Parameters
    ----------
    dataset : np.ndarray
        Samples used to fit the prior. For univariate data this can be a 1-D array of
        shape (n_samples,). For multivariate data, provide an array of shape (d, n_samples)
        (as expected by scipy.stats.gaussian_kde) or an array that can be transposed to
        that shape. The dataset must contain at least one sample.
    
    Attributes
    ----------
    kde : scipy.stats.kde.gaussian_kde
        The fitted kernel density estimator built from the provided dataset.

    """
    def __init__(self, dataset: np.ndarray):
        """
        Args:
            dataset (np.ndarray): Samples used to fit the prior. For univariate data this can be a 1-D array of
                shape (n_samples,). For multivariate data, provide an array of shape (d, n_samples)
                (as expected by scipy.stats.gaussian_kde) or an array that can be transposed to
                that shape. The dataset must contain at least one sample.
        """
        super().__init__()

        self.kde = gaussian_kde(dataset)
    
    def pdf(self, x):
        """Evaluate the estimated probability density at x. Accepts inputs compatible with
        scipy.stats.gaussian_kde.__call__: for univariate data x can be a float, 1-D array
        of points, or similarly shaped array for multivariate queries.
        
        Args:
            x (float | np.ndarray): point at which to evaluate the pdf
            
        Raises:
            ValueError:
                If `dataset` is empty.
            numpy.linalg.LinAlgError:
                If the covariance estimate used by gaussian_kde is singular (this is raised by
                scipy's implementation when the data are degenerate).
        """
        return self.kde(x)
        

class CustomPriorException(Exception):
    """This exception can be used is the custom prior
    is not correctly specified.

    It is usually raised if a non-normal prior is used
    that was not correctly inherited from the `CustomPrior` class.
    """
    pass
