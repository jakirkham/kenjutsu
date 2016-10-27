# -*- coding: utf-8 -*-

"""
The module ``kenjutsu`` provides support for working with ``slice``\ s.

===============================================================================
Overview
===============================================================================
The module ``kenjutsu`` provides several functions that are useful for working
with a Python ``slice`` or ``tuple`` of ``slice``\ s. This is of particular
value when working with NumPy_.

.. _NumPy: http://www.numpy.org/

===============================================================================
API
===============================================================================
"""


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Sep 08, 2016 15:46:46 EDT$"


import itertools
import operator
import math
import warnings


def reformat_slice(a_slice, a_length=None):
    """
        Takes a slice and reformats it to fill in as many undefined values as
        possible.

        Args:
            a_slice(slice):        a slice to reformat.

            a_length(int):         a length to fill for stopping if not
                                   provided.

        Returns:
            (slice):               a new slice with as many values filled in as
                                   possible.

        Examples:
            >>> reformat_slice(slice(None))
            slice(0, None, 1)

            >>> reformat_slice(slice(None), 10)
            slice(0, 10, 1)

            >>> reformat_slice(slice(2, None))
            slice(2, None, 1)

            >>> reformat_slice(slice(2, None), 10)
            slice(2, 10, 1)

            >>> reformat_slice(slice(2, None, None))
            slice(2, None, 1)

            >>> reformat_slice(slice(2, None, None), 10)
            slice(2, 10, 1)

            >>> reformat_slice(slice(2, -1, None), 10)
            slice(2, 9, 1)

            >>> range(10)[reformat_slice(slice(None))] == range(10)[:]
            True

            >>> range(10)[reformat_slice(slice(2, None))] == range(10)[2:]
            True

            >>> range(10)[reformat_slice(slice(2, 6))] == range(10)[2:6]
            True

            >>> range(10)[reformat_slice(slice(2, 6, 3))] == range(10)[2:6:3]
            True

            >>> range(10)[reformat_slice(slice(2, None, 3))] == range(10)[2::3]
            True

            >>> range(10)[reformat_slice(slice(None), 10)] == range(10)[:]
            True

            >>> range(10)[reformat_slice(slice(2, None), 10)] == range(10)[2:]
            True

            >>> range(10)[reformat_slice(slice(2, 6), 10)] == range(10)[2:6]
            True

            >>> range(10)[reformat_slice(slice(2, 6, 3), 10)] == range(10)[2:6:3]
            True

            >>> range(10)[reformat_slice(slice(2, None, 3), 10)] == range(10)[2::3]
            True

            >>> range(10)[reformat_slice(slice(2, -6, 3), 10)] == range(10)[2:-6:3]
            True

            >>> range(10)[reformat_slice(slice(2, -1), 10)] == range(10)[2:-1]
            True

            >>> range(10)[reformat_slice(slice(2, 20), 10)] == range(10)[2:20]
            True

            >>> range(10)[reformat_slice(slice(2, -20), 10)] == range(10)[2:-20]
            True

            >>> range(10)[reformat_slice(slice(20, -1), 10)] == range(10)[20:-1]
            True

            >>> range(10)[reformat_slice(slice(-20, -1), 10)] == range(10)[-20:-1]
            True

            >>> range(10)[reformat_slice(slice(-5, -1), 10)] == range(10)[-5:-1]
            True
    """

    assert (a_slice is not None), "err"

    # Fill unknown values.

    new_slice_step = a_slice.step
    if new_slice_step is None:
        new_slice_step = 1

    new_slice_start = a_slice.start
    if (new_slice_start is None) and (new_slice_step > 0):
        new_slice_start = 0

    new_slice_stop = a_slice.stop


    # Make adjustments for length

    if a_length is not None:
        if (new_slice_step < -a_length):
            new_slice_step = -a_length
        elif (new_slice_step > a_length):
            new_slice_step = a_length

        if (new_slice_start is None) and (new_slice_step > 0):
            pass
        elif (new_slice_start is None) and (new_slice_step < 0):
            new_slice_start = a_length
        elif (new_slice_start <= -a_length) and (new_slice_step > 0):
            new_slice_start = 0
        elif (new_slice_start < -a_length) and (new_slice_step < 0):
            new_slice_start = new_slice_stop = 0
        elif (new_slice_start > a_length) and (new_slice_step > 0):
            new_slice_start = a_length
        elif (new_slice_start > a_length) and (new_slice_step < 0):
            new_slice_start = a_length
        elif (new_slice_start < 0) and (new_slice_step > 0):
            new_slice_start += a_length
        elif (new_slice_start < 0) and (new_slice_step < 0):
            new_slice_start += a_length

        if (new_slice_stop is None) and (new_slice_step > 0):
            new_slice_stop = a_length
        elif (new_slice_stop is None) and (new_slice_step < 0):
            pass
        elif (new_slice_stop <= -a_length) and (new_slice_step > 0):
            new_slice_stop = 0
        elif (new_slice_stop < -a_length) and (new_slice_step < 0):
            new_slice_stop = None
        elif (new_slice_stop < 0) and (new_slice_step > 0):
            new_slice_stop += a_length
        elif (new_slice_stop < 0) and (new_slice_step < 0):
            new_slice_stop += a_length
        elif (new_slice_stop > a_length) and (new_slice_step > 0):
            new_slice_stop = a_length
        elif (new_slice_stop >= a_length) and (new_slice_step < 0):
            new_slice_start = new_slice_stop = 0
        elif (new_slice_stop < 0) and (new_slice_step > 0):
            new_slice_stop += a_length
        elif (new_slice_stop < 0) and (new_slice_step < 0):
            new_slice_stop += a_length


    # Build new slice and return.

    new_slice = slice(new_slice_start, new_slice_stop, new_slice_step)

    return(new_slice)


def reformat_slices(slices, lengths=None):
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

            >>> reformat_slices(slice(None))
            (slice(0, None, 1),)

            >>> reformat_slices((slice(None),))
            (slice(0, None, 1),)

            >>> reformat_slices((
            ...     slice(None),
            ...     slice(3, None),
            ...     slice(None, 5),
            ...     slice(None, None, 2)
            ... ))
            (slice(0, None, 1), slice(3, None, 1), slice(0, 5, 1), slice(0, None, 2))

            >>> reformat_slices(
            ...     (
            ...         slice(None),
            ...         slice(3, None),
            ...         slice(None, 5),
            ...         slice(None, None, 2)
            ...     ),
            ...     (10, 13, 15, 20)
            ... )
            (slice(0, 10, 1), slice(3, 13, 1), slice(0, 5, 1), slice(0, 20, 2))
    """

    try:
        len(slices)
    except TypeError:
        slices = (slices,)

    new_lengths = lengths
    if new_lengths is None:
        new_lengths = [None] * len(slices)

    try:
        len(new_lengths)
    except TypeError:
        new_lengths = (new_lengths,)

    assert (len(slices) == len(new_lengths))

    new_slices = list(slices)
    for i, each_length in enumerate(new_lengths):
        new_slices[i] = reformat_slice(new_slices[i], each_length)

    new_slices = tuple(new_slices)

    return(new_slices)


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
            >>> len_slice(slice(None)) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            UnknownSliceLengthException: Cannot determine slice length without a defined end point. The reformatted slice was slice(0, None, 1).

            >>> len_slice(slice(None), 10)
            10

            >>> len_slice(slice(None), 10) == len(range(10)[:])
            True

            >>> len_slice(slice(2, None), 10)
            8

            >>> len_slice(slice(2, None), 10) == len(range(10)[2:])
            True

            >>> len_slice(slice(2, None, None), 10)
            8

            >>> len_slice(slice(2, None, None), 10) == len(range(10)[2:])
            True

            >>> len_slice(slice(2, 6))
            4

            >>> len_slice(slice(2, 6), 1000)
            4

            >>> len_slice(slice(2, 6), 10) == len(range(10)[2:6])
            True

            >>> len_slice(slice(2, 6, 3))
            2

            >>> len_slice(slice(2, 6, 3), 10) == len(range(10)[2:6:3])
            True
    """

    new_slice = reformat_slice(a_slice, a_length)

    if new_slice.stop is None:
        raise UnknownSliceLengthException(
            "Cannot determine slice length without a defined end point. " +
            "The reformatted slice was " + repr(new_slice) + "."
        )

    new_slice_diff = float(new_slice.stop - new_slice.start)

    new_slice_size = int(math.ceil(new_slice_diff / new_slice.step))

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
            >>> len_slices((
            ...     slice(None),
            ...     slice(3, None),
            ...     slice(None, 5),
            ...     slice(None, None, 2)
            ... )) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            UnknownSliceLengthException: Cannot determine slice length without a defined end point. The reformatted slice was slice(0, None, 1).

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
        xrange
    except NameError:
        xrange = range

    try:
        from itertools import ifilter
        from itertools import imap
        from itertools import izip
    except ImportError:
        ifilter = filter
        imap = map
        izip = zip

    if block_halo is not None:
        assert (len(space_shape) == len(block_shape) == len(block_halo)), \
            "The dimensions of `space_shape`, `block_shape`, and " + \
            "`block_halo` should be the same."
    else:
        assert (len(space_shape) == len(block_shape)), \
            "The dimensions of `space_shape` and `block_shape` " + \
            "should be the same."

        block_halo = tuple()
        for i in xrange(len(space_shape)):
            block_halo += (0,)

    vec_add = lambda a, b: imap(operator.add, a, b)
    vec_sub = lambda a, b: imap(operator.sub, a, b)

    vec_mul = lambda a, b: imap(operator.mul, a, b)
    vec_div = lambda a, b: imap(operator.div, a, b)
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

    for each_dim in xrange(len(space_shape)):
        # Construct each block using the block size given. Allow to spill over.
        if block_shape[each_dim] == -1:
            block_shape = (block_shape[:each_dim] +
                           space_shape[each_dim:each_dim+1] +
                           block_shape[each_dim+1:])

        # Generate block ranges.
        a_range = []
        for i in xrange(2):
            offset = i * block_shape[each_dim]
            this_range = xrange(
                offset,
                offset + space_shape[each_dim],
                block_shape[each_dim]
            )
            a_range.append(list(this_range))

        # Add the halo to each block on both sides.
        a_range_haloed = []
        for i in xrange(2):
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
        for i in xrange(2):
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
