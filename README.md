<div align="left">
  <img src="https://raw.githubusercontent.com/sequential-parameter-optimization/spotdesirability/main/logo/spotlogo.png" alt="spotdesibility Logo" width="300">
</div>


# spotdesirability

## Features

### Version & License

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![GitHub Release](https://img.shields.io/github/v/release/sequential-parameter-optimization/spotdesirability)](https://github.com/sequential-parameter-optimization/spotdesirability/releases)
[![PyPI Version](https://img.shields.io/pypi/v/spotdesirability)](https://pypi.org/project/spotdesirability/)

[![License](https://img.shields.io/github/license/sequential-parameter-optimization/spotdesirability)](LICENSE)

### Downloads

[![PyPI Downloads](https://img.shields.io/pypi/dm/spotdesirability)](https://pypi.org/project/spotdesirability/)
[![Total Downloads](https://static.pepy.tech/badge/spotdesirability)](https://pepy.tech/project/spotdesirability)

### Quality

[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Ready-success)](MODEL_CARD.md)
[![Dependencies](https://img.shields.io/badge/dependencies-minimal-blue)](pyproject.toml)
[![Audit](https://img.shields.io/badge/audit-whitebox-brightgreen)](MODEL_CARD.md)
[![Reliability](https://img.shields.io/badge/robustness-fail--safe-orange)](MODEL_CARD.md)
[![Security](https://img.shields.io/badge/security-policy-blue)](https://sequential-parameter-optimization.github.io/spotdesirability/security/)

### Testing

[![CI Tests](https://img.shields.io/github/actions/workflow/status/sequential-parameter-optimization/spotdesirability/ci.yml?branch=main&label=CI%20Tests)](https://github.com/sequential-parameter-optimization/spotdesirability/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/actions/workflow/status/sequential-parameter-optimization/spotdesirability/release.yml?branch=main&label=Release)](https://github.com/sequential-parameter-optimization/spotdesirability/actions/workflows/release.yml)
[![Documentation](https://img.shields.io/github/actions/workflow/status/sequential-parameter-optimization/spotdesirability/docs.yml?branch=main&label=Docs)](https://github.com/sequential-parameter-optimization/spotdesirability/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/sequential-parameter-optimization/spotdesirability/branch/develop/graph/badge.svg)](https://codecov.io/gh/sequential-parameter-optimization/spotdesirability)
[![REUSE status](https://api.reuse.software/badge/github.com/sequential-parameter-optimization/spotdesirability)](https://api.reuse.software/info/github.com/sequential-parameter-optimization/spotdesirability)

### Scores (OpenSSF Scorecard)

[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/sequential-parameter-optimization/spotdesirability)](https://scorecard.dev/viewer/?uri=github.com/sequential-parameter-optimization/spotdesirability)



### Status

[![Maintenance](https://img.shields.io/badge/maintenance-active-green)](https://github.com/sequential-parameter-optimization/spotdesirability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## About

`spotdesirability` is a `Python` implementation of the `R` package `desirability`, which provides  S3 classes for multivariate optimization using the desirability function by Derringer and Suich (1980).

## Installation

Installation can be done with `pip`: 

```{bash}
pip install spotdesirability
```

or `uv`:

```{bash}
uv install spotdesirability
```

Alternatively, you can clone the repository and install it manually.

## Documentation

The documentation is available at: [https://sequential-parameter-optimization.github.io/spotdesirability/](https://sequential-parameter-optimization.github.io/spotdesirability/)


## Citation

```bibtex
@misc{bartz25a,
      title={Multi-Objective Optimization and Hyperparameter Tuning With Desirability Functions}, 
      author={Thomas Bartz-Beielstein},
      year={2025},
      eprint={2503.23595},
      archivePrefix={arXiv},
      primaryClass={math.OC},
      url={https://arxiv.org/abs/2503.23595}, 
}
```

## References

### Desirability functions

* Derringer, G., and Suich, R. Simultaneous optimization of several response variables. Journal of Quality Technology 12 (1980), 214–219.

### The `R` `desirability` package

* The `R` `desirability` package is maintained and developed by Max Kuhn. It is is available on CRAN:  https://CRAN.R-project.org/package=desirability,  DOI: https://doi.org/10.32614/CRAN.package.desirability
