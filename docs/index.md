# adaptivetesting

[![SPEC 0 — Minimum Supported Dependencies](docs/_static/SPEC-0.svg)](https://scientific-python.org/specs/spec-0000/)
![](https://anaconda.org/conda-forge/adaptivetesting/badges/version.svg)
![](https://anaconda.org/conda-forge/adaptivetesting/badges/license.svg)
![](https://anaconda.org/conda-forge/adaptivetesting/badges/downloads.svg)


![Logo of the adaptivetesting package](/docs/_static/logo.svg)


## Features

| **Ability Estimators** |                                                                                                                                                        |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Maximum Likelihood      | $\arg \max\, L(Y=1\| \theta)$                                                                                                                          |
| Bayes Modal             | $\arg \max \frac{L(\theta)P_\text{prior}(\theta)}{\int_\infty^\infty L(\theta)P_\text{prior}(\theta)}$                                                 |
| Expected a Posteriori   | $\frac{\int_{-\infty}^{\infty} \theta L(\theta) P_\text{prior}(\theta)\, d\theta}{\int_{-\infty}^{\infty} L(\theta) P_\text{prior}(\theta)\, d\theta}$ |
| **Item Selection**      |                                                                                                                                                        |
| MFI                     | $\arg \max I_i(\theta)$                                                                                                                                |
| **Exposure Control** |                                                                                                                                                        |
| Randomesque             |                                                                                                                               |
| Maximum Priority Index  | $PI_i = I_i \prod_{k=1}^K (w_k f_k)^{c_{ik}}$                                                                                                          |
| **Content Balancing** |                                                                                                                                                        |
| Maximum Priority Index  | $PI_i = I_i \prod_{k=1}^K (w_k f_k)^{c_{ik}}$                                                                                                          |
| Weighted Penalty Model  | $F_i = w'F_i' + w'' F_i''$                                                                                                                             |
| **Stopping Criterion** |                                                                                                                                                        |
| Standard Error          | $\leq \frac{1}{\sqrt{I(\theta)}}$                                                                                                                      |
| Test Length             | $\#\, \text{of items} $                                                                                                                                |
