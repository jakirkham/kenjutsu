from __future__ import absolute_import


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 16:20:14 GMT-0500$"


import kenjutsu.format
import kenjutsu.measure


def join_slice(slice_1, slice_2, length=None):
    """
        Joins the two slices into one.

        Applying the resulting slice should have the same effect as applying
        the two slices in order.

        Args:
            slice_1(slice):                   first slice to apply
            slice_2(slice):                   second slice to apply
            length(int):                      length of each dimension of the
                                              object to slice.

        Returns:
            (slice):                          one slice equivalent to applying
                                              the two slices in order.

        Examples:

            >>> join_slice(slice(2, None), slice(None, 10))
            slice(2, 10, 1)
    """

    rf_slice_1 = kenjutsu.format.reformat_slice(slice_1, length)

    len_slice_1 = None
    try:
        len_slice_1 = kenjutsu.measure.len_slice(rf_slice_1)
    except kenjutsu.measure.UnknownSliceLengthException:
        pass

    rf_slice_2 = kenjutsu.format.reformat_slice(slice_2, len_slice_1)

    result_slice_step = rf_slice_1.step * rf_slice_2.step
    if result_slice_step > 0:
        result_slice_start = rf_slice_1.start + rf_slice_2.start
        if rf_slice_1.stop is None:
            result_slice_stop = rf_slice_2.stop
        elif rf_slice_2.stop is None:
            result_slice_stop = rf_slice_1.stop
        else:
            result_slice_stop = rf_slice_1.stop - rf_slice_2.stop
    else:
        result_slice_start = rf_slice_1.start - rf_slice_2.start + 2
        if rf_slice_1.stop is None:
            result_slice_stop = rf_slice_2.stop
        elif rf_slice_2.stop is None:
            result_slice_stop = rf_slice_1.stop
        else:
            result_slice_stop = rf_slice_1.stop + rf_slice_2.stop

    result_slice = slice(result_slice_start,
                         result_slice_stop,
                         result_slice_step)

    return result_slice
