"""
Warning:
    The module ``kenjutsu.kenjutsu`` is deprecated. Please use
    ``kenjutsu.core`` instead.
"""

from __future__ import absolute_import


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Sep 08, 2016 15:46:46 EDT$"


import warnings


warnings.warn(
    "Please use `kenjutsu.core` instead.",
    DeprecationWarning
)


def reformat_slice(a_slice, a_length=None):
    """
        Takes a slice and reformats it to fill in as many undefined values as
        possible.

        Warning:
            This function is deprecated. Please use
            ``kenjutsu.core.reformat_slice`` instead.

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

    warnings.warn(
        "Please use `kenjutsu.core.reformat_slice` instead.",
        DeprecationWarning
    )

    from kenjutsu import core

    return core.reformat_slice(a_slice, a_length)


def reformat_slices(slices, lengths=None):
    """
        Takes a tuple of slices and reformats them to fill in as many undefined
        values as possible.

        Warning:
            This function is deprecated. Please use
            ``kenjutsu.core.reformat_slices`` instead.

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

    warnings.warn(
        "Please use `kenjutsu.core.reformat_slices` instead.",
        DeprecationWarning
    )

    from kenjutsu import core

    return core.reformat_slices(slices, lengths)


from kenjutsu.core import UnknownSliceLengthException


def len_slice(a_slice, a_length=None):
    """
        Determines how many elements a slice will contain.

        Warning:
            This function is deprecated. Please use
            ``kenjutsu.core.len_slice`` instead.

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

    warnings.warn(
        "Please use `kenjutsu.core.len_slice` instead.",
        DeprecationWarning
    )

    from kenjutsu import core

    return core.len_slice(a_slice, a_length)


def len_slices(slices, lengths=None):
    """
        Takes a tuple of slices and reformats them to fill in as many undefined
        values as possible.

        Warning:
            This function is deprecated. Please use
            ``kenjutsu.core.len_slices`` instead.

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

    warnings.warn(
        "Please use `kenjutsu.core.len_slices` instead.",
        DeprecationWarning
    )

    from kenjutsu import core

    return core.len_slices(slices, lengths)


def split_blocks(space_shape, block_shape, block_halo=None):
    """
        Return a list of slicings to cut each block out of an array or other.

        Takes an array with ``space_shape`` and ``block_shape`` for every
        dimension and a ``block_halo`` to extend each block on each side. From
        this, it can compute slicings to use for cutting each block out from
        the original array, HDF5 dataset or other.

        Warning:
            This function is deprecated. Please use
            ``kenjutsu.core.split_blocks`` instead.

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

    warnings.warn(
        "Please use `kenjutsu.core.split_blocks` instead.",
        DeprecationWarning
    )

    from kenjutsu import core

    return core.split_blocks(space_shape, block_shape, block_halo)
