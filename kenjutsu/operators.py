from __future__ import absolute_import

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 16:20:14 GMT-0500$"

import collections
import itertools
import numbers

import kenjutsu.format


def split_multindex(slices):
    """
        Splits slices with multiple indices into multiple splices.

        Support of slices with a sequence of indices is varied. Some
        libraries like NumPy support them without issues. Other libraries
        like h5py support them as long as they are in sequential order.
        In still other libraries support is non-existent. However, in
        all those cases normally a single index is permissible. This
        converts slices with multiple indices into a list of slices with
        a single index each. While this still leaves it up to the user
        to iterate over these and combine the results in some sensible
        way, it is better than just getting a failure and should extend
        well to a variety of cases.

        Args:
            slices(tuple(slice)):        a tuple of slices to split

        Returns:
            (list(tuple(slice))):        a list of a tuple of slices

        Examples:

            >>> split_multindex(
            ...     (
            ...         3,
            ...         Ellipsis,
            ...         [0, 1, 2],
            ...         slice(2, 5),
            ...         slice(4, 6, 2)
            ...     )
            ... )  # doctest: +NORMALIZE_WHITESPACE
            [(3, Ellipsis, 0, slice(2, 5, 1), slice(4, 6, 2)),
             (3, Ellipsis, 1, slice(2, 5, 1), slice(4, 6, 2)),
             (3, Ellipsis, 2, slice(2, 5, 1), slice(4, 6, 2))]
    """

    ref_slices = kenjutsu.format.reformat_slices(slices)

    mtx_slices = []
    for each_dim_slice in ref_slices:
        if each_dim_slice is Ellipsis:
            mtx_slices.append([each_dim_slice])
        elif isinstance(each_dim_slice, numbers.Integral):
            mtx_slices.append([each_dim_slice])
        elif isinstance(each_dim_slice, slice):
            mtx_slices.append([each_dim_slice])
        elif isinstance(each_dim_slice, collections.Sequence):
            mtx_slices.append(list(each_dim_slice))

    result_slices = []
    for each_dim_slice in itertools.product(*mtx_slices):
        result_slices.append(tuple(each_dim_slice))

    return result_slices
