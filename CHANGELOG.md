# Version 1.2
- Required Python version: >= 3.12
- The package now follows SPEC0
- All functions can be now be imported from the top-level namespace
- Adding descriptive statistics and plotting functions
- Added support for the GRM and GPCM models (polytomous response variables)
- Added `SkewNormalPrior` and `EmpiricalPrior` for Bayesian ability estimation
- Added support for Content Balancing and Exposure Control
- The package is now also published on conda-forge

*Note*: We have tried our best to eliminate breaking changes. 
But still, please be careful when updating to this version.
# Version 1.1.6
- Bug Fig #49 (optimization interval issue in BayesModal)

# Version 1.1.5
- Bug Fix #46 (numerical stability issue concerning Bayesian ability estimation)

# Version 1.1.4
- Bug Fix #43 (optimization interval in `maximize_posterior` function)

# Version 1.1.3
- Bug Fix #34 (numerical stability issue concerning the ability estimation and standard error calculation)

# Version 1.1.2

- The `ItemPool` class now correctly honors the `id` field of items. (#30, #31)
- Examples and the readme file have been updated accordingly.
