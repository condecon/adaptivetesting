# adaptivetesting
[![Unittests](https://github.com/condecon/adaptivetesting/actions/workflows/python-test.yml/badge.svg)](https://github.com/condecon/adaptivetesting/actions/workflows/python-test.yml)
[![Deploy to PyPi](https://github.com/condecon/adaptivetesting/actions/workflows/publish.yml/badge.svg)](https://github.com/condecon/adaptivetesting/actions/workflows/publish.yml)

_adaptivetesting_ is a Python package for computer-aided adaptive 
testing that can be used to simulate and implement custom adaptive tests 
in real-world testing scenarios.

## Getting Started

Required Python version: >= 3.11 (other versions may work, but they are not officially supported)

``
pip install git+https://github.com/condecon/adaptivetesting
``

Other dependencies:
- numpy

## Features
- Rasch Model
- fast Maximum Likelihood Estimation of the current ability
- Item selection with Urry's rule
- __Fully customizable testing behavior__

The package comes with two testing procedures:
- Default implementation
- Semi-Adaptive implementation

Custom testing procedures can be implemented by implementing
the abstract class ``AdaptiveTest``.
Any existing functionality can be overridden while still
retaining full compatability with the packages' functionality.
For more information, please consult the documentation for the ``AdaptiveTest`` class
([``AdaptiveTest`` documentation](/documentation/adaptivetesting.models.txt)).

## Implementations
### Default implementation

![Schematic overview of the Default implementation](/images/default.svg)

### Semi-Adaptive implementation
![Schematic overview of the Semi-Adaptive implementation](/images/semi-adaptive.svg)

## Documentation
Extensive documentation of all programm code is available at [`/documentation`](/documentation).
