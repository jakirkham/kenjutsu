from __future__ import absolute_import


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 15:26:16 GMT-0500$"


import itertools
import math
import operator
import warnings

import kenjutsu.format


def num_blocks(space_shape, block_shape):
    """
        Computes the number of blocks.

        Takes an array with ``space_shape`` and ``block_shape`` for every
        dimension. From this, it can compute slicings to use for cutting
        each block out from the original array, HDF5 dataset, or other.


        Args:
            space_shape(tuple):            Shape of array to slice
            block_shape(tuple):            Size of each block to take

        Returns:
            tuple:                         Number of blocks per dimension

        Examples:

            >>> num_blocks(
            ...     (2, 3,), (2, 1,)
            ... )  #doctest: +NORMALIZE_WHITESPACE
            (1, 3)

    """

    try:
        irange = xrange
    except NameError:
        irange = range

    try:
        from itertools import ifilter, imap
    except ImportError:
        ifilter, imap = filter, map

    if not (len(space_shape) == len(block_shape)):
        raise ValueError(
            "The dimensions of `space_shape` and `block_shape` should be"
            " the same."
        )

    if not all(imap(lambda e: e > 0, space_shape)):
        raise ValueError(
            "Shape of the space must all be positive definite."
            "Instead got: %s." % str(space_shape)
        )

    if not all(imap(lambda e: e > 0 or e == -1, block_shape)):
        raise ValueError(
            "Shape of the blocks must all be positive or -1."
            "Instead got: %s." % str(block_shape)
        )

    vec_type = lambda t, a: imap(t, a)

    vec_ceil = lambda a: imap(math.ceil, a)

    vec_div = lambda a, b: imap(operator.truediv, a, b)
    vec_mod = lambda a, b: imap(operator.mod, a, b)

    vec_nonzero = lambda a: \
            imap(lambda _: _[0], ifilter(lambda _: _[1], enumerate(a)))
    vec_str = lambda a: imap(str, a)

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

    for each_dim in irange(len(space_shape)):
        # Construct each block using the block size given. Allow to spill over.
        if block_shape[each_dim] == -1:
            block_shape = (block_shape[:each_dim] +
                           space_shape[each_dim:each_dim+1] +
                           block_shape[each_dim+1:])

    n_blocks = vec_type(int, vec_ceil(vec_div(space_shape, block_shape)))

    return tuple(n_blocks)


def split_blocks(space_shape, block_shape, block_halo=None, index=None):
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
            index(bool):                   Whether to provide an index for
                                           each block

        Returns:
            collections.Sequence of \
            tuples of slices:              Provides tuples of slices for \
                                           retrieving blocks.

        Examples:

            >>> split_blocks(
            ...     (2, 3,), (1, 1,), (1, 1,), True
            ... )  #doctest: +NORMALIZE_WHITESPACE
            ([(0, 0),
              (0, 1),
              (0, 2),
              (1, 0),
              (1, 1),
              (1, 2)],
            <BLANKLINE>
             [(slice(0, 1, 1), slice(0, 1, 1)),
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

    if index is None:
        index = False
        warnings.warn(
            "`index` will default to `True` in the next minor release.",
            FutureWarning
        )
    else:
        warnings.warn(
            "`index` will be deprecated in the next minor release. Once"
            " removed, `split_blocks` will act as if `index` were `True`.",
            PendingDeprecationWarning
        )

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

    if not all(imap(lambda e: e > 0, space_shape)):
        raise ValueError(
            "Shape of the space must all be positive definite."
            "Instead got: %s." % str(space_shape)
        )

    if not all(imap(lambda e: e > 0 or e == -1, block_shape)):
        raise ValueError(
            "Shape of the blocks must all be positive or -1."
            "Instead got: %s." % str(block_shape)
        )

    if not all(imap(lambda e: e >= 0, block_halo)):
        raise ValueError(
            "Shape of the halo must all be positive semidefinite."
            "Instead got: %s." % str(block_halo)
        )

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
        a_range = kenjutsu.format.reformat_slices(a_range)
        a_range_haloed = kenjutsu.format.reformat_slices(a_range_haloed)
        a_trimmed_halo = kenjutsu.format.reformat_slices(a_trimmed_halo)

        # Collect all blocks
        ranges_per_dim.append(a_range)
        haloed_ranges_per_dim.append(a_range_haloed)
        trimmed_halos_per_dim.append(a_trimmed_halo)

    # Take all combinations of all ranges to get blocks.
    result = tuple()
    if index:
        index_blocks = imap(lambda e: irange(len(e)), ranges_per_dim)
        index_blocks = list(itertools.product(*index_blocks))
        result += (index_blocks,)

    orig_blocks = list(itertools.product(*ranges_per_dim))
    haloed_blocks = list(itertools.product(*haloed_ranges_per_dim))
    trimmed_halos = list(itertools.product(*trimmed_halos_per_dim))

    result += (orig_blocks, haloed_blocks, trimmed_halos)

    return result
