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


import math


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


def blocks_split(space_shape, block_shape, block_halo=None):
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
            space_shape(numpy.ndarray):    Shape of array to slice
            block_shape(numpy.ndarray):    Size of each block to take
            block_halo(numpy.ndarray):     Halo to tack on to each block

        Returns:
            collections.Sequence of \
            tuples of slices:              Provides tuples of slices for \
                                           retrieving blocks.

        Examples:
            >>> blocks_split(
            ...     (2,), (1,)
            ... )  #doctest: +NORMALIZE_WHITESPACE
            ([(slice(0, 1, 1),), (slice(1, 2, 1),)],
            <BLANKLINE>
             [(slice(0, 1, 1),), (slice(1, 2, 1),)],
            <BLANKLINE>
             [(slice(0, 1, 1),), (slice(0, 1, 1),)])

            >>> blocks_split((2,), (-1,))
            ([(slice(0, 2, 1),)], [(slice(0, 2, 1),)], [(slice(0, 2, 1),)])

            >>> blocks_split(
            ...     (2, 3,), (1, 1,)
            ... )  #doctest: +NORMALIZE_WHITESPACE
            ([(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
            <BLANKLINE>
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
            <BLANKLINE>
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1))])

            >>> blocks_split(
            ...     (2, 3,), (1, 1,), (0, 0,)
            ... )  #doctest: +NORMALIZE_WHITESPACE
            ([(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
            <BLANKLINE>
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
            <BLANKLINE>
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1))])

            >>> blocks_split(
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


            >>> blocks_split(
            ...     (10, 12,), (3, 2,), (4, 3,)
            ... )  #doctest: +NORMALIZE_WHITESPACE
            ([(slice(0, 3, 1), slice(0, 2, 1)),
              (slice(0, 3, 1), slice(2, 4, 1)),
              (slice(0, 3, 1), slice(4, 6, 1)),
              (slice(0, 3, 1), slice(6, 8, 1)),
              (slice(0, 3, 1), slice(8, 10, 1)),
              (slice(0, 3, 1), slice(10, 12, 1)),
              (slice(3, 6, 1), slice(0, 2, 1)),
              (slice(3, 6, 1), slice(2, 4, 1)),
              (slice(3, 6, 1), slice(4, 6, 1)),
              (slice(3, 6, 1), slice(6, 8, 1)),
              (slice(3, 6, 1), slice(8, 10, 1)),
              (slice(3, 6, 1), slice(10, 12, 1)),
              (slice(6, 9, 1), slice(0, 2, 1)),
              (slice(6, 9, 1), slice(2, 4, 1)),
              (slice(6, 9, 1), slice(4, 6, 1)),
              (slice(6, 9, 1), slice(6, 8, 1)),
              (slice(6, 9, 1), slice(8, 10, 1)),
              (slice(6, 9, 1), slice(10, 12, 1)),
              (slice(9, 10, 1), slice(0, 2, 1)),
              (slice(9, 10, 1), slice(2, 4, 1)),
              (slice(9, 10, 1), slice(4, 6, 1)),
              (slice(9, 10, 1), slice(6, 8, 1)),
              (slice(9, 10, 1), slice(8, 10, 1)),
              (slice(9, 10, 1), slice(10, 12, 1))],
            <BLANKLINE>
             [(slice(0, 7, 1), slice(0, 5, 1)),
              (slice(0, 7, 1), slice(0, 7, 1)),
              (slice(0, 7, 1), slice(1, 9, 1)),
              (slice(0, 7, 1), slice(3, 11, 1)),
              (slice(0, 7, 1), slice(5, 12, 1)),
              (slice(0, 7, 1), slice(7, 12, 1)),
              (slice(0, 10, 1), slice(0, 5, 1)),
              (slice(0, 10, 1), slice(0, 7, 1)),
              (slice(0, 10, 1), slice(1, 9, 1)),
              (slice(0, 10, 1), slice(3, 11, 1)),
              (slice(0, 10, 1), slice(5, 12, 1)),
              (slice(0, 10, 1), slice(7, 12, 1)),
              (slice(2, 10, 1), slice(0, 5, 1)),
              (slice(2, 10, 1), slice(0, 7, 1)),
              (slice(2, 10, 1), slice(1, 9, 1)),
              (slice(2, 10, 1), slice(3, 11, 1)),
              (slice(2, 10, 1), slice(5, 12, 1)),
              (slice(2, 10, 1), slice(7, 12, 1)),
              (slice(5, 10, 1), slice(0, 5, 1)),
              (slice(5, 10, 1), slice(0, 7, 1)),
              (slice(5, 10, 1), slice(1, 9, 1)),
              (slice(5, 10, 1), slice(3, 11, 1)),
              (slice(5, 10, 1), slice(5, 12, 1)),
              (slice(5, 10, 1), slice(7, 12, 1))],
            <BLANKLINE>
              [(slice(0, 3, 1), slice(0, 2, 1)),
               (slice(0, 3, 1), slice(2, 4, 1)),
               (slice(0, 3, 1), slice(3, 5, 1)),
               (slice(0, 3, 1), slice(3, 5, 1)),
               (slice(0, 3, 1), slice(3, 5, 1)),
               (slice(0, 3, 1), slice(3, 5, 1)),
               (slice(3, 6, 1), slice(0, 2, 1)),
               (slice(3, 6, 1), slice(2, 4, 1)),
               (slice(3, 6, 1), slice(3, 5, 1)),
               (slice(3, 6, 1), slice(3, 5, 1)),
               (slice(3, 6, 1), slice(3, 5, 1)),
               (slice(3, 6, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(0, 2, 1)),
               (slice(4, 7, 1), slice(2, 4, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(0, 2, 1)),
               (slice(4, 7, 1), slice(2, 4, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(3, 5, 1)),
               (slice(4, 7, 1), slice(3, 5, 1))])

    """

    space_shape = numpy.array(space_shape)
    block_shape = numpy.array(block_shape)

    if block_halo is not None:
        block_halo = numpy.array(block_halo)

        assert (space_shape.ndim == block_shape.ndim == block_halo.ndim == 1),\
            "There should be no more than 1 dimension for " + \
            "`space_shape`, `block_shape`, and `block_halo`."
        assert (len(space_shape) == len(block_shape) == len(block_halo)), \
            "The dimensions of `space_shape`, `block_shape`, and " + \
            "`block_halo` should be the same."
    else:
        assert (space_shape.ndim == block_shape.ndim == 1), \
            "There should be no more than 1 dimension for " + \
            "`space_shape` and `block_shape`."
        assert (len(space_shape) == len(block_shape)), \
            "The dimensions of `space_shape` and `block_shape` " + \
            "should be the same."

        block_halo = numpy.zeros_like(space_shape)

    uneven_block_division = (space_shape % block_shape != 0)

    if uneven_block_division.any():
        uneven_block_division_str = uneven_block_division.nonzero()[0].tolist()
        uneven_block_division_str = [str(_) for _ in uneven_block_division_str]
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

    for each_dim in iters.irange(len(space_shape)):
        # Construct each block using the block size given. Allow to spill over.
        if block_shape[each_dim] == -1:
            block_shape[each_dim] = space_shape[each_dim]

        a_range = numpy.arange(0, space_shape[each_dim], block_shape[each_dim])
        a_range = expand_view(a_range, reps_before=2).copy()
        a_range[1] += block_shape[each_dim]

        # Add the halo to each block on both sides.
        a_range_haloed = a_range.copy()
        a_range_haloed[1] += block_halo[each_dim]
        a_range_haloed[0] -= block_halo[each_dim]
        a_range_haloed.clip(0, space_shape[each_dim], out=a_range_haloed)

        # Compute how to trim the halo off of each block.
        # Clip each block to the boundaries.
        a_trimmed_halo = numpy.empty_like(a_range)
        a_trimmed_halo[...] = a_range - a_range_haloed[0]
        a_range.clip(0, space_shape[each_dim], out=a_range)

        # Transpose to allow for iteration over each block's dimension.
        a_range = a_range.T.copy()
        a_range_haloed = a_range_haloed.T.copy()
        a_trimmed_halo = a_trimmed_halo.T.copy()

        # Convert all ranges to slices for easier use.
        a_range = iters.reformat_slices([
            slice(*a_range[i]) for i in iters.irange(len(a_range))
        ])
        a_range_haloed = iters.reformat_slices([
            slice(*a_range_haloed[i]) for i in iters.irange(len(a_range_haloed))
        ])
        a_trimmed_halo = iters.reformat_slices([
            slice(*a_trimmed_halo[i]) for i in iters.irange(len(a_trimmed_halo))
        ])

        # Collect all blocks
        ranges_per_dim.append(a_range)
        haloed_ranges_per_dim.append(a_range_haloed)
        trimmed_halos_per_dim.append(a_trimmed_halo)

    # Take all combinations of all ranges to get blocks.
    blocks = list(itertools.product(*ranges_per_dim))
    haloed_blocks = list(itertools.product(*haloed_ranges_per_dim))
    trimmed_halos = list(itertools.product(*trimmed_halos_per_dim))

    return(blocks, haloed_blocks, trimmed_halos)
