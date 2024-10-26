# adaptivetesting
_adaptivetesting_ is a Python package for Computerized Adaptive Testing
that can be used for simulating as well as implementing adaptive tests
into real testing scenarios.

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

## Implementations
### Default implementation

![Schematic overview of the Default implementation](/images/default.svg)

### Semi-Adaptive implementation
![Schematic overview of the Semi-Adaptive implementation](/images/semi-adaptive.svg)

## Documentation
Extensive documentation of all programm code is available at [`/documentation`](/documentation).
