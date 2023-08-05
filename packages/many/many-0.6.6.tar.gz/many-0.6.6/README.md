# many

This package provides a general-use toolkit for frequently-implemented statistical and visual methods. See the [blog post](https://kevinhu.io/2020/09/17/many.html) for an explanation of the purpose of this package and the methods used.

**[Full documentation](https://many.kevinhu.io)**

## Installation

```bash
pip install many
```

Note: if you want to use CUDA-accelerated statistical methods (i.e. `many.stats.mat_mwu_gpu`), you must also independently install the corresponding version of [cupy](https://github.com/cupy/cupy).

## Components

### Statistical methods

The statistical methods comprise several functions for association mining between variable pairs. These methods are optimized for `pandas` DataFrames and are inspired by the `corrcoef` function provided by `numpy`.

Because these functions rely on native matrix-level operations provided by `numpy`, many are orders of magnitude faster than naive looping-based alternatives. This makes them useful for constructing large association networks or for feature extraction, which have important uses in areas such as biomarker discovery. All methods also return estimates of statistical significance.

In certain cases such as the computation of correlation coefficients, **these vectorized methods come with the caveat of [numerical instability](https://stats.stackexchange.com/questions/94056/instability-of-one-pass-algorithm-for-correlation-coefficient)**. As a compromise, "naive" loop-based implementations are also provided for testing and comparison. It is recommended that any significant results obtained with the vectorized methods be verified with these base methods.

The current functions available are listed below by variable comparison type. Benchmarks are also provided with comparisons to the equivalent looping-based method. In all methods, a `melt` option is provided to return the outputs as a set of row-column variable-variable pair statistic matrices or as a single `DataFrame` with each statistic melted to a column.

### Visual methods

Several visual methods are also included for interpretation of results from the statistical methods. Like the statistical methods, these are also grouped by variable types plotted.

## Development

1. Install dependencies with `poetry install`
2. Initialize environment with `poetry shell`
3. Initialize pre-commit hooks with `pre-commit install`
