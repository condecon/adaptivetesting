# adaptivetesting
[![Unittests](https://github.com/condecon/adaptivetesting/actions/workflows/python-test.yml/badge.svg)](https://github.com/condecon/adaptivetesting/actions/workflows/python-test.yml)
[![Deploy to PyPi](https://github.com/condecon/adaptivetesting/actions/workflows/publish.yml/badge.svg)](https://github.com/condecon/adaptivetesting/actions/workflows/publish.yml)

<img src="/docs_generation/source/_static/logo.svg" style="width: 100%">
</img>

_adaptivetesting_ is a Python package for computerized adaptive 
testing that can be used to simulate and implement custom adaptive tests 
in real-world testing scenarios.

## Getting Started

Required Python version: >= 3.11 (other versions may work, but they are not officially supported)

``
pip install adaptivetesting
``

If you want to install the current development version,
you can do so by running the following command:

``
pip install git+https://github.com/condecon/adaptivetesting
``

## Features
- IRT-Models: 
    - 4PL
    - simplified derivates (e.g., 3PL, Rasch model)
- Ability estimators: 
    - Maximum Likelihood Estimation
    - Bayes Modal
- Item selection algorithm: 
    - Urry’s rule
- Stopping criteria: 
    - test length
    - ability estimation standard error
- Test results output formats
    - SQLITE
    - Pickle
- Functions and wrappers for CAT simulations and application implementations

__Any functionality can be modified and extended.__


## Implementations
The package comes with two CAT implementations that are ready to use.
### Default implementation

![Schematic overview of the Default implementation](/images/default.svg)

### Semi-Adaptive implementation
![Schematic overview of the Semi-Adaptive implementation](/images/semi-adaptive.svg)

### Custom testing procedures
Custom testing procedures can be implemented by implementing
the abstract class ``AdaptiveTest``.
Any existing functionality can be overridden while still
retaining full compatibility with the packages' functionality.
For more information, please consult the documentation for the ``AdaptiveTest`` class.

## Package structure
| submodule | description |
|------------|-------------|
| data | data management and processing of test results |
| implementations | concrete implementations of the adaptive process, provides actual |
| math | mathematical utilities and functions, such as estimators, item selection, test information |
| models | data model definitions and structures used in the package |
| services | interfaces that concrete implementations inherit from |
| simulations | functions and classes used in CAT simulation |
| tests | Unit test for the entire package |

## Documentation

You can find extensiv documentation in the <a href="/docs/">`docs` directory</a>.