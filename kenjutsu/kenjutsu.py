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
import numbers
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

            >>> reformat_slice(slice(2, -1, None))
            slice(2, -1, 1)

            >>> reformat_slice(slice(2, -1, None), 10)
            slice(2, 9, 1)
    """

    new_slice = a_slice
    if (new_slice is Ellipsis) or (new_slice == tuple()):
        new_slice = slice(None)
    elif isinstance(a_slice, numbers.Integral):
        if a_slice < 0:
            new_slice = slice(a_slice, a_slice-1, -1)
        else:
            new_slice = slice(a_slice, a_slice+1, 1)
    elif not isinstance(a_slice, slice):
        raise ValueError(
            "Expected a `slice` type. Instead got `%s`." % str(a_slice)
        )

    if new_slice.step == 0:
        raise ValueError("Slice cannot have a step size of `0`.")

    start = new_slice.start
    stop = new_slice.stop
    step = new_slice.step

    # Fill unknown values.
    if step is None:
        step = 1
    if start is None:
        if step > 0:
            start = 0
        elif step < 0:
            start = -1
    if (stop is None) and (step > 0):
        stop = a_length

    stop_i = stop is not None

    # Make adjustments for length
    if a_length is not None:
        # Normalize out-of-bound step sizes.
        if step < -a_length:
            step = -a_length
        elif step > a_length:
            step = a_length

        # Normalize bounded negative values.
        if -a_length <= start < 0:
            start += a_length
        if stop_i and (-a_length <= stop < 0):
            stop += a_length

        # Handle out-of-bound limits.
        if step > 0:
            if (start > a_length) or (stop < -a_length):
                start = stop = 0
                step = 1
            else:
                if start < -a_length:
                    start = 0
                if stop > a_length:
                    stop = a_length
        elif step < 0:
            if (start < -a_length) or (stop_i and stop >= (a_length - 1)):
                start = stop = 0
                step = 1
            else:
                if start >= a_length:
                    start = a_length - 1
                if stop_i and stop < -a_length:
                    stop = None
                    stop_i = False

    # Catch some known empty slices.
    if stop_i and (start == stop):
        start = stop = 0
        step = 1
    elif (step > 0) and (stop == 0):
        start = stop = 0
        step = 1
    elif (step < 0) and (stop == -1):
        start = stop = 0
        step = 1
    elif stop_i and (start >= 0) and (stop >= 0):
        if (step > 0) and (start > stop):
            start = stop = 0
            step = 1
        elif (step < 0) and (start < stop):
            start = stop = 0
            step = 1

    new_slice = slice(start, stop, step)
    if isinstance(a_slice, numbers.Integral):
        if new_slice.start == new_slice.stop == 0:
            raise IndexError("Index out of range.")
        new_slice = new_slice.start

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

    new_slices = slices
    if new_slices == tuple():
        new_slices = Ellipsis

    try:
        len(new_slices)
    except TypeError:
        new_slices = (new_slices,)

    new_lengths = lengths
    try:
        if new_lengths is not None:
            len(new_lengths)
    except TypeError:
        new_lengths = (new_lengths,)

    el_idx = None
    try:
        el_idx = new_slices.index(Ellipsis)
    except ValueError:
        pass

    if new_lengths is not None and el_idx is None:
        if len(new_slices) != len(new_lengths):
            raise ValueError("Shape must be the same as the number of slices.")
    elif new_lengths is not None:
        if (len(new_slices) - 1) > len(new_lengths):
            raise ValueError(
                "Shape must be as large or larger than the number of slices"
                " without the Ellipsis."
            )

    if el_idx is not None:
        # Break into three cases.
        #
        # 1. Before the Ellipsis
        # 2. The Ellipsis
        # 3. After the Ellipsis
        #
        # Cases 1 and 3 are trivially solved as before.
        # Case 2 is either a no-op or a bunch of `slice(None)`s.
        #
        # The result is a combination of all of these.

        slices_before = new_slices[:el_idx]
        slices_after = new_slices[el_idx+1:]

        if Ellipsis in slices_before or Ellipsis in slices_after:
            raise ValueError("Only one Ellipsis is permitted. Found multiple.")

        new_lengths_before = None
        new_lengths_after = None
        slice_el = (Ellipsis,)
        if new_lengths is not None:
            pos_before = len(slices_before)
            pos_after = len(new_lengths) - len(slices_after)

            new_lengths_before = new_lengths[:pos_before]
            new_lengths_after = new_lengths[pos_after:]

            new_lengths_el = new_lengths[pos_before:pos_after]
            slice_el = len(new_lengths_el) * (slice(None),)
            if slice_el:
                slice_el = reformat_slices(
                    slice_el,
                    new_lengths_el
                )

        if slices_before:
            slices_before = reformat_slices(slices_before, new_lengths_before)
        if slices_after:
            slices_after = reformat_slices(slices_after, new_lengths_after)

        new_slices = slices_before + slice_el + slices_after
    else:
        if new_lengths is None:
            new_lengths = [None] * len(new_slices)

        new_slices = list(new_slices)
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

    if new_slice.stop is None:
        if new_slice.step > 0:
            raise UnknownSliceLengthException(
                "Cannot determine slice length without a defined end point. " +
                "The reformatted slice was " + repr(new_slice) + "."
            )
        else:
            new_slice = slice(new_slice.start, -1, new_slice.step)

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
