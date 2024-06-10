#%%%
import matplotlib.pyplot as plt
import numpy as np
import adaptivetesting.math


#%%%
response_pattern = np.array([1,0,1])
difficulties = np.array([0.4, 0.1, 0.3])

def log_likelihood_1d(ability: np.ndarray) -> np.ndarray:
    item_terms = response_pattern - 1 + (1 / (np.exp(ability - difficulties) + 1))

    return np.cumsum(item_terms)[len(item_terms) - 1]


#%%%
abilities = np.linspace(-10, 10, 1000)

#%%%
estimator = adaptivetesting.math.MLEstimator(
    response_pattern, difficulties
)

#%%%
lik_res = []
for ability in abilities:
    lik_res.append(estimator.log_likelihood(ability))
lik_res = np.array(lik_res)

#%%%
lik_d1_res = []
for ability in abilities:
    lik_d1_res.append(log_likelihood_1d(ability))
lik_d1_res = np.array(lik_d1_res)

#%%%
fig, ax = plt.subplots()

ax.scatter(abilities, lik_res)
ax.scatter(abilities, lik_d1_res)