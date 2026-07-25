# adaptivetesting

<img src="/docs/_static/logo.svg" style="width: 100%">
</img>

**An open-source Python package for simplified, customizable Computerized Adaptive Testing (CAT) using Bayesian methods.**


## Key Features

- **Bayesian Methods**: Built-in support for Bayesian ability estimation with customizable priors
- **Flexible Architecture**: Object-oriented design with abstract classes for easy extension
- **Item Response Theory**: Full support for 1PL, 2PL, 3PL, and 4PL models, GRM, GPCM
- **Multiple Estimators**:
  - Maximum Likelihood Estimation (MLE)
  - Bayesian Modal Estimation (BM)
  - Expected A Posteriori (EAP)
- **Item Selection Strategies**: Maximum information criterion
- **Content Balancing**: Maximum Priority Index, Weighted Penalty Model
- **Exposure Control**: Randomesque Item Selection, Maximum Priority Index 
- **Simulation Framework**: Comprehensive tools for CAT simulation and evaluation
- **Real-world Application**: Direct transition from simulation to production testing
- **Stopping Criteria**: Support for standard error and test length criteria
- **Data Management**: Built-in support for CSV and pickle data formats

## Installation

Install from PyPI using pip:

```bash
pip install adaptivetesting
```

For the latest development version:

```bash
pip install git+https://github.com/condecon/adaptivetesting
```

## Documentation
You can find our documentation in the [GitHub wiki](https://github.com/condecon/adaptivetesting/wiki).

## Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/condecon/adaptivetesting) for:

- Issue tracking
- Feature requests
- Pull request guidelines
- Development setup

## Research and Applications

This package is designed for researchers and practitioners in:

- Educational assessment
- Psychological testing
- Cognitive ability measurement
- Adaptive learning systems
- Psychometric research

The package facilitates the transition from research simulation to real-world testing applications without requiring major code modifications.

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

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
