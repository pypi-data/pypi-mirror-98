"""
Continuous binning sketch.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2021

import numbers

import numpy as np

from ...preprocessing import split_data
from .bsketch import _check_parameters
from .bsketch import _indices_count
from .gk import GK

try:
    from tdigest import TDigest
    TDIGEST_AVAILABLE = True
except ImportError:
    TDIGEST_AVAILABLE = False


class ContinuousBSketch:
    """ContinuousBSketch: binning sketch for numerical values and continuous
    target.

    Parameters
    ----------
    sketch : str, optional (default="gk")
        Sketch algorithm. Supported algorithms are "gk" (Greenwald-Khanna's)
        and "t-digest" (Ted Dunning) algorithm. Algorithm "t-digest" relies on
        `tdigest <https://github.com/CamDavidsonPilon/tdigest>`_.

    eps : float (default=0.01)
        Relative error epsilon.

    K : int (default=25)
        Parameter excess growth K to compute compress threshold in t-digest.

    special_codes : array-like or None, optional (default=None)
        List of special codes. Use special codes to specify the data values
        that must be treated separately.
    """
    def __init__(self, sketch="gk", eps=0.01, K=25, special_codes=None):
        self.sketch = sketch
        self.eps = eps
        self.K = K
        self.special_codes = special_codes

        _check_parameters(sketch, eps, K, special_codes)

        self._count_missing = 0
        self._count_special = 0

        if sketch == "gk":
            self._sketch = GK(eps)
        elif sketch = "t-digest":
            self._sketch = TDigest(eps, K)

    def add(self, x, y, check_input=False):
        """Add arrays to the sketch.

        Parameters
        ----------
        x : array-like, shape = (n_samples,)
            Training vector, where n_samples is the number of samples.

        y : array-like, shape = (n_samples,)
            Target vector relative to x.

        check_input : bool (default=False)
            Whether to check input arrays.
        """
        xc, yc, xm, ym, xs, ys, _, _, _, _, _, _, _ = split_data(
            dtype=None, x=x, y=y, special_codes=self.special_codes,
            check_input=check_input)

        # Add values to sketch

        if self.sketch == "gk":
            for v in xc:
                self._sketch.add(v)

        if self.sketch == "t-digest":
            self._sketch.batch_update(xc)

        # Keep track of missing and special counts
        self._count_missing += len(ym)
        self._count_special += len(ys)

    def bins(self, splits):
        """Record counts for each bin given a list of split points.

        Parameters
        ----------
        splits : array-like, shape = (n_splits,)
            List of split points.

        Returns
        -------
        bins : arrays of size n_splits + 1.
        """        
        n_bins = len(splits) + 1
        bins_ = np.zeros(n_bins).astype(np.int64)

        indices, count = _indices_count(self.sketch, self._sketch, splits)

        for i in range(n_bins):
            bins_[i] = count[(indices == i)].sum()

        return bins_

    def merge(self, bsketch):
        """Merge current instance with another BSketch instance.

        Parameters
        ----------
        bsketch : object
            ContinuousBSketch instance.
        """
        if not self._mergeable(bsketch):
            raise Exception("bsketch does not share signature.")

        if bsketch._sketch.n == 0:
            return

        if self._sketch.n == 0:
            self._copy(bsketch)
            return        

        # Merge sketches
        if self.sketch == "gk":
            self._sketch.merge(bsketch._sketch)
        elif self.sketch == "t-digest":
            self._sketch += bsketch._sketch

        # Merge missing and special counts
        self._count_missing += bsketch._count_missing
        self._count_special += bsketch._count_special

    def _copy(self, bsketch):
        self._sketch = bsketch._sketch

        # Merge missing and special counts
        self._count_missing = bsketch._count_missing
        self._count_special = bsketch._count_special

    def _mergeable(self, other):
        special_eq = True
        if self.special_codes is not None and other.special_codes is not None:
            special_eq = set(self.special_codes) == set(other.special_codes)

        return (self.sketch == other.sketch and self.eps == other.eps and
                self.K == other.K and special_eq)

    @property
    def n(self):
        """Records count.

        Returns
        -------
        n : int
        """
        return self._sketch.n


class ContinuousBCatSketch:
    """ContinuousBCatSketch: binning sketch for categorical/nominal data and
    continuous target.

    Parameters
    ----------
    cat_cutoff : float or None, optional (default=None)
        Generate bin others with categories in which the fraction of
        occurrences is below the  ``cat_cutoff`` value.

    special_codes : array-like or None, optional (default=None)
        List of special codes. Use special codes to specify the data values
        that must be treated separately.
    """
    def __init__(self, cat_cutoff=None, special_codes=None):
        self.cat_cutoff = cat_cutoff
        self.special_codes = special_codes

        if cat_cutoff is not None:
            if (not isinstance(cat_cutoff, numbers.Number) or
                    not 0. < cat_cutoff <= 1.0):
                raise ValueError("cat_cutoff must be in (0, 1.0]; got {}."
                                 .format(cat_cutoff))

        if special_codes is not None:
            if not isinstance(special_codes, (np.ndarray, list)):
                raise TypeError(
                    "special_codes must be a list or numpy.ndarray.")

        self._count_missing = 0
        self._count_special = 0

        self._d_categories = {}

    def add(self, x, y, check_input=False):
        """Add arrays to the sketch.

        Parameters
        ----------
        x : array-like, shape = (n_samples,)
            Training vector, where n_samples is the number of samples.

        y : array-like, shape = (n_samples,)
            Target vector relative to x.

        check_input : bool (default=False)
            Whether to check input arrays.
        """
        xc, yc, xm, ym, xs, ys, _, _, _, _, _, _, _ = split_data(
            dtype=None, x=x, y=y, special_codes=self.special_codes,
            check_input=check_input)

        # Add values to sketch
        for i, c in enumerate(xc):
            if c in self._d_categories:
                self._d_categories[c] += 1
            else:
                self._d_categories[c] = 1

        # Keep track of missing and special counts
        self._count_missing += len(ym)
        self._count_special += len(ys)

    def bins(self):
        """Record counts for each bin given the current categories.

        Returns
        -------
        bins : tuple of arrays.
        """

    def merge(self, bcatsketch):
        pass

    def _mergeable(self, other):
        special_eq = True
        if self.special_codes is not None and other.special_codes is not None:
            special_eq = set(self.special_codes) == set(other.special_codes)

        return special_eq

    @property
    def n(self):
        """Records count.

        Returns
        -------
        n : int
        """
        return np.sum([v for k, v in self._d_categories.items()])
