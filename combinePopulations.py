# -*- coding: utf-8 -*-
from __future__ import division
import unittest


def combineTwoUnivariatePopulations(m1, v1, n1, m2, v2, n2):
    """Combine two populations' sample means and variances.

    Given `m1`, `v1`, `n1`, the sample mean μ, sample variance σ², and
    sample size, respectively, of one population, and similarly `m2`,
    `v2`, and `n2` of a second population, returns the combined
    populations' sample mean and variance as a tuple of three values
    containing the combined sample mean, sample variance, and size.
    
    See https://stats.stackexchange.com/a/43183"""
    m = (m1 * n1 + m2 * n2) / (n1 + n2)
    v = (n1 * (v1 + m1 * m1) + n2 * (v2 + m2 * m2)) / (n1 + n2) - m * m
    return (m, v, n1 + n2)


def combineTwoBivariatePopulations(x1, y1, Cov1, n1, x2, y2, Cov2, n2):
    """Combine two bivariate populations' sample means and covariances.

    Given `x1`, `y1`, `Cov1`, and `n1`, the sample mean of variable X,
    the sample mean of variable Y, the two by two sample covariance
    matrix of X versus Y, and the sample size, of one population, 
    respectively, and similarly `x2`, `y2`, `Cov2`, and `n2` of a
    second population, returns the combined populations' sample mean
    and covariance as a 4-tuple containing
    
    1. the combined sample mean of variable X,
    2. ditto for Y,
    3. the combined sample covariance between X and Y, and
    4. the combined population's size.
    
    See botom of [1], starting with

    > Likewise, there is a formula for combining the covariances of two sets...
    
    [1] https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=829952267#Online"""
    x3, vx3, n3 = combineTwoUnivariatePopulations(x1, Cov1[0][0], n1, x2,
                                                  Cov2[0][0], n2)
    y3, vy3, _ = combineTwoUnivariatePopulations(y1, Cov1[1][1], n1, y2,
                                                 Cov2[1][1], n2)
    Ca = Cov1[0][1] * n1
    Cb = Cov2[0][1] * n2  # Cov[0][1] == Cov[1][0] by symmetry
    Cc = Ca + Cb + (x1 - x2) * (y1 - y2) * n1 * n2 / n3
    c = Cc / n3
    Cov3 = ([[vx3, c], [c, vy3]])
    return (x3, y3, Cov3, n3)


class Test(unittest.TestCase):
    def testCombinecov(self):
        import numpy as np

        first = combineTwoBivariatePopulations(1, 20, np.zeros((2, 2)), 1, 2,
                                               21.1, np.zeros((2, 2)), 1)
        firstCov = np.cov([[1, 2.], [20, 21.1]], bias=True)
        self.assertTrue(
            np.allclose(first[2], firstCov),
            msg='Two bivariate populations of size one')

        secondCov = np.cov([[1, 2, -1.1], [20, 21.1, 19.5]], bias=True)
        second = combineTwoBivariatePopulations(*(
            first + (-1.1, 19.5, np.zeros((2, 2)), 1)))
        self.assertTrue(
            np.allclose(second[2], secondCov),
            msg='Combine populations of size three and one')

        thirdCov = np.cov(
            [[1, 2, 1, 2, -1.1], [20, 21.1, 20, 21.1, 19.5]], bias=True)
        third = combineTwoBivariatePopulations(*(first + second))
        self.assertTrue(
            np.allclose(third[2], thirdCov),
            msg='Populations of size two and three (recursive)')

        full = np.random.randn(2, 5)
        fullCov = np.cov(full, bias=True)
        combined = combineTwoBivariatePopulations(
            np.mean(full[0, :2]), np.mean(full[1, :2]),
            np.cov(full[:, :2], bias=True), 2, np.mean(full[0, 2:]),
            np.mean(full[1, 2:]), np.cov(full[:, 2:], bias=True), 3)
        self.assertTrue(
            np.allclose(combined[2], fullCov),
            msg='Populations of size two and three')
        return True


if __name__ == '__main__':
    unittest.main()
