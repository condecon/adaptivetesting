# adaptivetesting
![Logo of the adaptivetesting package](_static/logo.svg)

![Following SPEC 0](_static/spec0.svg)
![Supported Python Versions](_static/python.svg)
![Package Repositories: PyPi, conda-forge](_static/package.svg)

## Features

* **IRT Models**
  * 4PL, 3PL, 2PL, Rasch
  * GRM
  * GPCM
* **Ability Estimators**
  * Maximum Likelihood
  * Bayes Modal 
  * Expected a Posteriori  
* **Item Selection**
  * MFI
* **Exposure Control**
  * Randomesque
  * Maximum Priority Index
* **Content Balancing**
  * Maximum Priority Index
  * Weighted Penalty Model
  * **Stopping Criterion**
  * Standard Error
  * Test Length


## Package Installation
### PyPi

```bash
pip install adaptivetesting
```

### Conda
```bash
conda install conda-forge::adaptivetesting
```

## Citation
If you use this package for your academic work, please provide the following reference:
Engicht, J., Bee, R.M. & Koch, T. Customizable Bayesian adaptive testing with Python – The adaptivetesting package. Behav Res 58, 250 (2026). https://doi.org/10.3758/s13428-026-03079-w

```
@Article{Engicht2026,
author="Engicht, Jonas
and Bee, R. Maximilian
and Koch, Tobias",
title="Customizable Bayesian adaptive testing with Python -- The adaptivetesting package",
journal="Behavior Research Methods",
year="2026",
month="Jul",
day="24",
volume="58",
number="9",
pages="250",
abstract="This paper introduces an open-source Python package for simplified, customizable computerized adaptive testing (CAT) using Bayesian methods for ability estimation. It addresses the lack of sophisticated packages for CAT in the Python programming language. Moreover, it bridges the gap between the construction and simulation of adaptive tests and their practical application by providing a dedicated API for integration with experiment software. Thereby, it eliminates the need for major code rewrites when transitioning from simulated to real-world adaptive testing. By leveraging Python's object-oriented programming approach, such as abstract classes, protocols, and inheritance, the package allows for easy extension and customization of its functionality. For example, Bayesian estimators can be modified to incorporate custom priors. This paper outlines the relevance and practical use of the adaptivetesting package through a walkthrough example. The package is fully documented, and its source code is published on GitHub. It is also available on the Python Package Index (PyPi) and conda-forge thus it can easily be installed using Python's package manager pip or conda. Leveraging R's reticulate package, adaptivetesting can also be accessed from within RStudio.",
issn="1554-3528",
doi="10.3758/s13428-026-03079-w",
url="https://doi.org/10.3758/s13428-026-03079-w"
}


```