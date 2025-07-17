# Breaking Changes in `adaptivetesting`

This document highlights breaking changes and updates in the `adaptivetesting` package, considering its structure, features, and potential impacts on users transitioning between versions.

## 1. Python Version Requirement
- **Updated Requirement**: Python version `>= 3.11` is now required. Users on Python 3.10 or earlier may experience compatibility issues.

## 2. Package Structure
- The package is organized into several key modules:
  - **`adaptivetesting.models`**: Core classes including `AdaptiveTest`, `ItemPool`, and `TestItem`.
  - **`adaptivetesting.implementations`**: Ready-to-use test implementations like `TestAssembler`.
  - **`adaptivetesting.math`**: Mathematical functions for IRT, ability estimation, and item selection.
  - **`adaptivetesting.simulation`**: Simulation framework and result management.
  - **`adaptivetesting.data`**: Data management utilities for CSV and pickle formats.
  - **`adaptivetesting.services`**: Abstract interfaces and protocols.

## 3. Key Features
- **Bayesian Methods**: Built-in support for Bayesian ability estimation with customizable priors.
- **Flexible Architecture**: Object-oriented design with abstract classes for easy extension.
- **Item Response Theory**: Full support for 1PL, 2PL, 3PL, and 4PL models.
- **Multiple Estimators**: 
  - Maximum Likelihood Estimation (MLE)
  - Bayesian Modal Estimation (BM)
  - Expected A Posteriori (EAP)
- **Item Selection Strategies**: Maximum information criterion and Urry's rule.
- **Simulation Framework**: Comprehensive tools for CAT simulation and evaluation.
- **Real-world Application**: Direct transition from simulation to production testing.
- **Stopping Criteria**: Support for standard error and test length criteria.
- **Data Management**: Built-in support for CSV and pickle data formats.

## 4. Installation Instructions
- Install from PyPI using pip:
  ```bash
  pip install adaptivetesting
  ```
- For the latest development version:
  ```bash
  pip install git+https://github.com/condecon/adaptivetesting
  ```

## 5. Requirements
- The following dependencies are required:
  - Python >= 3.11
  - NumPy >= 2.0.0
  - Pandas >= 2.2.0
  - SciPy >= 1.15.0
  - tqdm >= 4.67.1

## 6. Documentation Updates
- Full documentation is available in the `docs/` directory:
  - [API Reference](docs/readme.md)
  - [Models Module](docs/adaptivetesting.models.md)
  - [Math Module](docs/adaptivetesting.math.md)
  - [Implementation Examples](docs/adaptivetesting.implementations.md)
  - [Simulation Guide](docs/adaptivetesting.simulation.md)

## 7. Testing
- Comprehensive tests are included. Run them using:
  ```bash
  python -m pytest adaptivetesting/tests/
  ```

---

**Action Required**: Users should review these changes and update their environments and workflows accordingly.
