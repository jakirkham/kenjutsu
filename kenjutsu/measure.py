from __future__ import absolute_import

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 14:49:29 GMT-0500$"


import numbers
import math

import kenjutsu.format


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

    new_slice = kenjutsu.format.reformat_slice(a_slice, a_length)

    new_slice_size = 0
    if isinstance(new_slice, slice):
        if (new_slice.step > 0 and new_slice.start >= 0 and
                (new_slice.stop is None or new_slice.stop < 0)):
                raise UnknownSliceLengthException(
                    "Cannot determine slice length without a defined end"
                    " point. The reformatted slice was %s." % repr(new_slice)
                )
        elif (new_slice.step < 0 and new_slice.start < 0 and
                (new_slice.stop is None or new_slice.stop >= 0)):
                raise UnknownSliceLengthException(
                    "Cannot determine slice length without a defined start"
                    " point. The reformatted slice was %s." % repr(new_slice)
                )

        if new_slice.step < 0 and new_slice.stop is None:
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

    new_slices = kenjutsu.format.reformat_slices(slices, lengths)

    lens = []

    for each_slice in new_slices:
        if not isinstance(each_slice, numbers.Integral):
            lens.append(len_slice(each_slice))

    lens = tuple(lens)

    return(lens)
