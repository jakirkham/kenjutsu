from __future__ import absolute_import

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 16:20:14 GMT-0500$"


import collections
import math
import numbers

import kenjutsu.format
import kenjutsu.measure


def reverse_slice(a_slice, a_len=None):
    """
        Reverses the direction of a slice.

        Args:
            a_slice(slice):        a slice to reformat.
            a_len(int):            length of the object being sliced(optional).

        Returns:
            (slice):               a new slice that gets the reverse.

        Examples:

            >>> reverse_slice(slice(9, 2, -3))
            slice(3, 12, 3)
    """

    new_slice = kenjutsu.format.reformat_slice(a_slice, a_len)

    if isinstance(new_slice, numbers.Integral):
        return new_slice
    elif isinstance(new_slice, collections.Sequence):
        return list(reversed(new_slice))

    len_slice = kenjutsu.measure.len_slice(new_slice)

    # Update stop position.
    stop = new_slice.stop
    stop = -1 if new_slice.step < 0 and stop is None else stop
    n_steps = int(math.ceil(
        float(stop - new_slice.start) / float(new_slice.step)
    ))
    start = stop - n_steps * new_slice.step

    new_slice = slice(stop + 1, start + 1, -new_slice.step)
    new_slice = kenjutsu.format.reformat_slice(new_slice, a_len)

    return(new_slice)
