from jax.scipy.stats import norm

class Prior:
    def pdf(self, x):
        raise NotImplementedError

class Normal(Prior):
    def __init__(self, mean=0, std=1):
        self.mean = mean
        self.std = std

    def pdf(self, x):
        return norm.pdf(x, loc=self.mean, scale=self.std)