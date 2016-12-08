# -*- coding: utf-8 -*-

"""
The module ``core`` provides support for working with ``slice``\ s.

===============================================================================
Overview
===============================================================================
The module ``core`` provides several functions that are useful for working
with a Python ``slice`` or ``tuple`` of ``slice``\ s. This is of particular
value when working with NumPy_.

.. _NumPy: http://www.numpy.org/

===============================================================================
API
===============================================================================
"""


from __future__ import absolute_import


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 11:35:58 GMT-0500$"


import itertools
import numbers
import operator
import math
import warnings

import kenjutsu.format


reformat_slice = kenjutsu.format.reformat_slice
reformat_slices = kenjutsu.format.reformat_slices


class UnknownSliceLengthException(Exception):
    """
        Raised if a slice does not have a known length.
    """

    pass


def len_slice(a_slice, a_length=None):
    """
        Determines how many elements a slice will contain.

        Raises:
            UnknownSliceLengthException: Will raise an exception if
            a_slice.stop and a_length is None.

        Args:
            a_slice(slice):        a slice to reformat.

            a_length(int):         a length to fill for stopping if not
                                   provided.

        Returns:
            (slice):               a new slice with as many values filled in as
                                   possible.

        Examples:

            >>> len_slice(slice(2, None), 10)
            8

            >>> len_slice(slice(2, 6))
            4
    """

    if isinstance(a_slice, numbers.Integral):
        raise TypeError(
            "An integral index does not provide an object with a length."
        )

    new_slice = reformat_slice(a_slice, a_length)

    new_slice_size = 0
    if isinstance(new_slice, slice):
        if new_slice.stop is None:
            if new_slice.step > 0:
                raise UnknownSliceLengthException(
                    "Cannot determine slice length without a defined end"
                    " point. The reformatted slice was %s." % repr(new_slice)
                )
            else:
                new_slice = slice(new_slice.start, -1, new_slice.step)

        new_slice_diff = float(new_slice.stop - new_slice.start)

        new_slice_size = int(math.ceil(new_slice_diff / new_slice.step))
    else:
        new_slice_size = len(new_slice)

    return(new_slice_size)


def len_slices(slices, lengths=None):
    """
        Takes a tuple of slices and reformats them to fill in as many undefined
        values as possible.

        Args:
            slices(tuple(slice)):        a tuple of slices to reformat.
            lengths(tuple(int)):         a tuple of lengths to fill.

        Returns:
            (slice):                     a tuple of slices with all default
                                         values filled if possible.

        Examples:

            >>> len_slices(
            ...     (
            ...         slice(None),
            ...         slice(3, None),
            ...         slice(None, 5),
            ...         slice(None, None, 2)
            ...     ),
            ...     (10, 13, 15, 20)
            ... )
            (10, 10, 5, 10)
    """

    new_slices = reformat_slices(slices, lengths)

    lens = []

    for each_slice in new_slices:
        if not isinstance(each_slice, numbers.Integral):
            lens.append(len_slice(each_slice))

    lens = tuple(lens)

    return(lens)


def split_blocks(space_shape, block_shape, block_halo=None):
    """
        Return a list of slicings to cut each block out of an array or other.

        Takes an array with ``space_shape`` and ``block_shape`` for every
        dimension and a ``block_halo`` to extend each block on each side. From
        this, it can compute slicings to use for cutting each block out from
        the original array, HDF5 dataset or other.

        Note:
            Blocks on the boundary that cannot extend the full range will
            be truncated to the largest block that will fit. This will raise
            a warning, which can be converted to an exception, if needed.

        Args:
            space_shape(tuple):            Shape of array to slice
            block_shape(tuple):            Size of each block to take
            block_halo(tuple):             Halo to tack on to each block

        Returns:
            collections.Sequence of \
            tuples of slices:              Provides tuples of slices for \
                                           retrieving blocks.

        Examples:

            >>> split_blocks(
            ...     (2, 3,), (1, 1,), (1, 1,)
            ... )  #doctest: +NORMALIZE_WHITESPACE
            ([(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
            <BLANKLINE>
             [(slice(0, 2, 1), slice(0, 2, 1)),
              (slice(0, 2, 1), slice(0, 3, 1)),
              (slice(0, 2, 1), slice(1, 3, 1)),
              (slice(0, 2, 1), slice(0, 2, 1)),
              (slice(0, 2, 1), slice(0, 3, 1)),
              (slice(0, 2, 1), slice(1, 3, 1))],
            <BLANKLINE>
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(1, 2, 1))])

    """

    try:
        irange = xrange
    except NameError:
        irange = range

    try:
        from itertools import ifilter, imap
    except ImportError:
        ifilter, imap = filter, map

    if block_halo is not None:
        if not (len(space_shape) == len(block_shape) == len(block_halo)):
            raise ValueError(
                "The dimensions of `space_shape`, `block_shape`, and"
                " `block_halo` should be the same."
            )
    else:
        if not (len(space_shape) == len(block_shape)):
            raise ValueError(
               "The dimensions of `space_shape` and `block_shape` should be"
               " the same."
            )

        block_halo = tuple()
        for i in irange(len(space_shape)):
            block_halo += (0,)

    vec_add = lambda a, b: imap(operator.add, a, b)
    vec_sub = lambda a, b: imap(operator.sub, a, b)

    vec_mul = lambda a, b: imap(operator.mul, a, b)
    vec_mod = lambda a, b: imap(operator.mod, a, b)

    vec_nonzero = lambda a: \
            imap(lambda _: _[0], ifilter(lambda _: _[1], enumerate(a)))
    vec_str = lambda a: imap(str, a)

    vec_clip_floor = lambda a, a_min: \
            imap(lambda _: _ if _ >= a_min else a_min, a)
    vec_clip_ceil = lambda a, a_max: \
            imap(lambda _: _ if _ <= a_max else a_max, a)
    vec_clip = lambda a, a_min, a_max: \
            vec_clip_ceil(vec_clip_floor(a, a_min), a_max)

    uneven_block_division = tuple(vec_mod(space_shape, block_shape))

    if any(uneven_block_division):
        uneven_block_division_str = vec_nonzero(uneven_block_division)
        uneven_block_division_str = vec_str(uneven_block_division_str)
        uneven_block_division_str = ", ".join(uneven_block_division_str)

        warnings.warn(
            "Blocks will not evenly divide the array." +
            " The following dimensions will be unevenly divided: %s." %
            uneven_block_division_str,
            RuntimeWarning
        )

    ranges_per_dim = []
    haloed_ranges_per_dim = []
    trimmed_halos_per_dim = []

    for each_dim in irange(len(space_shape)):
        # Construct each block using the block size given. Allow to spill over.
        if block_shape[each_dim] == -1:
            block_shape = (block_shape[:each_dim] +
                           space_shape[each_dim:each_dim+1] +
                           block_shape[each_dim+1:])

        # Generate block ranges.
        a_range = []
        for i in irange(2):
            offset = i * block_shape[each_dim]
            this_range = irange(
                offset,
                offset + space_shape[each_dim],
                block_shape[each_dim]
            )
            a_range.append(list(this_range))

        # Add the halo to each block on both sides.
        a_range_haloed = []
        for i in irange(2):
            sign = 2 * i - 1

            haloed = vec_mul(
                itertools.repeat(sign, len(a_range[i])),
                itertools.repeat(block_halo[each_dim], len(a_range[i])),
            )
            haloed = vec_add(a_range[i], haloed)
            haloed = vec_clip(haloed, 0, space_shape[each_dim])

            a_range_haloed.append(list(haloed))

        # Compute how to trim the halo off of each block.
        # Clip each block to the boundaries.
        a_trimmed_halo = []
        for i in irange(2):
            trimmed = vec_sub(a_range[i], a_range_haloed[0])
            a_trimmed_halo.append(list(trimmed))
            a_range[i] = list(vec_clip(a_range[i], 0, space_shape[each_dim]))

        # Convert all ranges to slices for easier use.
        a_range = tuple(imap(slice, *a_range))
        a_range_haloed = tuple(imap(slice, *a_range_haloed))
        a_trimmed_halo = tuple(imap(slice, *a_trimmed_halo))

        # Format all slices.
        a_range = reformat_slices(a_range)
        a_range_haloed = reformat_slices(a_range_haloed)
        a_trimmed_halo = reformat_slices(a_trimmed_halo)

        # Collect all blocks
        ranges_per_dim.append(a_range)
        haloed_ranges_per_dim.append(a_range_haloed)
        trimmed_halos_per_dim.append(a_trimmed_halo)

    # Take all combinations of all ranges to get blocks.
    blocks = list(itertools.product(*ranges_per_dim))
    haloed_blocks = list(itertools.product(*haloed_ranges_per_dim))
    trimmed_halos = list(itertools.product(*trimmed_halos_per_dim))

    return(blocks, haloed_blocks, trimmed_halos)
