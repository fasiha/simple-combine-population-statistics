# simple-combine-population-statistics

Pure Python (3 and 2) module to combine the sample means and (co)variances from two populations into a single population mean and (co)variance. Handles the univariate case (i.e., deals with sample variances) and the bivariate case (where covariance is a two by two nested array (Numpy array works too but Numpy isn't needed)).

## Unit test
Run the built-in unit test (*test depends on Numpy!*) from the command line:
```
$ python combinePopulations.py
.
----------------------------------------------------------------------
Ran 1 test in 0.006s

OK
```

## Install
Drop the [raw Python file](combinePopulations.py) into your module's directory and `import combinePopulations`. Numpy is *only* used in the unit test.

## Usage
### `combineTwoUnivariatePopulations(m1, v1, n1, m2, v2, n2)`
Combine two populations' sample means and variances.

Given `m1`, `v1`, `n1`, the sample mean μ, sample variance σ², and sample size, respectively, of one population, and similarly `m2`, `v2`, and `n2` of a second population, returns the combined populations' sample mean and variance as a tuple of three values containing the combined sample mean, sample variance, and size.

Algorithm courtesy of @whuber at https://stats.stackexchange.com/a/43183.

### `combineTwoBivariatePopulations(x1, y1, Cov1, n1, x2, y2, Cov2, n2)`
Combine two bivariate populations' sample means and covariances.

Given `x1`, `y1`, `Cov1`, and `n1`, the sample mean of variable X, the sample mean of variable Y, the two by two sample covariance matrix of X versus Y, and the sample size, of one population,  respectively, and similarly `x2`, `y2`, `Cov2`, and `n2` of a second population, returns the combined populations' sample mean and covariance as a 4-tuple containing
1. the combined sample mean of variable X,
2. ditto for Y,
3. the combined sample covariance between X and Y, and
4. the combined population's size.

Source: See bottom of Wikipedia, ["Algorithms for calculating variance"](https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=829952267#Online), the paragraph starting with

> Likewise, there is a formula for combining the covariances of two sets...

### Notes
Numpy is not required in the core functions, so feel free to use a nested array like `[[1.0, 0.1], [0.1, 2.0]]` or a Numpy version for covariances.

Using [`functools.reduce`](https://docs.python.org/3/library/functools.html#functools.reduce), you can readily make versions that apply to more than two populations. (I don't know how to make it work for more than two variables though.)
