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
Engicht, J., Bee, R. M., & Koch, T. (2025). Customizable Bayesian Adaptive Testing with Python – The adaptivetesting Package. Open Science Framework. https://doi.org/10.31219/osf.io/d2xge_v1

```
@online{engichtCustomizableBayesianAdaptive2025,
  title = {Customizable {{Bayesian Adaptive Testing}} with {{Python}} – {{The}} Adaptivetesting {{Package}}},
  author = {Engicht, Jonas and Bee, R. Maximilian and Koch, Tobias},
  date = {2025-08-06},
  eprinttype = {Open Science Framework},
  doi = {10.31219/osf.io/d2xge_v1},
  url = {https://osf.io/d2xge_v1},
  pubstate = {prepublished}
}
```

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
