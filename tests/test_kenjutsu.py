#!/usr/bin/env python

# -*- coding: utf-8 -*-


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Oct 02, 2016 15:38:07 EDT$"


import doctest
import itertools
import math
import operator
import sys
import unittest

from kenjutsu import kenjutsu


try:
    irange = xrange
except NameError:
    irange = range


# Load doctests from `kenjutsu`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(kenjutsu))
    return tests


class TestKenjutsu(unittest.TestCase):
    def setUp(self):
        pass


    def test_reformat_slice(self):
        with self.assertRaises(TypeError) as e:
            kenjutsu.reformat_slice(None)

        self.assertEqual(
            str(e.exception),
            "Expected an index acceptable type."
            " Instead got, `None`."
        )

        with self.assertRaises(ValueError) as e:
            kenjutsu.reformat_slice(slice(None, None, 0))

        self.assertEqual(
            str(e.exception),
            "Slice cannot have a step size of `0`."
        )

        with self.assertRaises(TypeError) as e:
            kenjutsu.reformat_slice([None])

        self.assertEqual(
            str(e.exception),
            "Arbitrary sequences not permitted."
            " All elements must be of integral type."
        )

        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)

            for start in itertools.chain([None], irange(-excess, excess)):
                for stop in itertools.chain([None], irange(-excess, excess)):
                    for step in itertools.chain(irange(-excess, excess)):
                        step = None if step == 0 else step

                        a_slice = slice(start, stop, step)

                        rf_slice = kenjutsu.reformat_slice(a_slice)
                        self.assertEqual(
                            each_range[a_slice],
                            each_range[rf_slice]
                        )

                        rf_slice = kenjutsu.reformat_slice(a_slice, size)
                        self.assertEqual(
                            each_range[a_slice],
                            each_range[rf_slice]
                        )

                        new_start = rf_slice.start
                        new_stop = rf_slice.stop
                        new_step = rf_slice.step

                        if (new_step is not None and
                            new_step < 0 and
                            new_stop is None):
                            new_stop = -1

                        l = float(new_stop - new_start)/float(new_step)
                        self.assertEqual(
                            int(math.ceil(l)),
                            len(each_range[a_slice])
                        )

                        a_slice = list()
                        a_slice.append(0 if start is None else start)
                        a_slice.append(0 if stop is None else stop)
                        a_slice.append(0 if step is None else step)

                        a_op = operator.itemgetter(*a_slice)

                        expected_result = None
                        try:
                            expected_result = a_op(each_range)
                        except IndexError:
                            pass

                        if expected_result is not None:
                            rf_slice = kenjutsu.reformat_slice(a_slice)
                            rf_op = operator.itemgetter(*rf_slice)
                            self.assertEqual(
                                expected_result,
                                rf_op(each_range)
                            )

                            rf_slice = kenjutsu.reformat_slice(a_slice, size)
                            rf_op = operator.itemgetter(*rf_slice)
                            self.assertEqual(
                                expected_result,
                                rf_op(each_range)
                            )
                        else:
                            kenjutsu.reformat_slice(a_slice)
                            with self.assertRaises(IndexError):
                                kenjutsu.reformat_slice(a_slice, size)

                if start is not None:
                    a_slice = start

                    expected_result = None
                    try:
                        expected_result = each_range[a_slice]
                    except IndexError:
                        pass

                    if expected_result is not None:
                        rf_slice = kenjutsu.reformat_slice(a_slice)
                        self.assertEqual(
                            expected_result,
                            each_range[rf_slice]
                        )

                        rf_slice = kenjutsu.reformat_slice(a_slice, size)
                        self.assertEqual(
                            expected_result,
                            each_range[rf_slice]
                        )
                    else:
                        kenjutsu.reformat_slice(a_slice)
                        with self.assertRaises(IndexError):
                            kenjutsu.reformat_slice(a_slice, size)

            rf_slice = kenjutsu.reformat_slice(Ellipsis)
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            rf_slice = kenjutsu.reformat_slice(Ellipsis, size)
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            rf_slice = kenjutsu.reformat_slice(tuple())
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            rf_slice = kenjutsu.reformat_slice(tuple(), size)
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            start = rf_slice.start
            stop = rf_slice.stop
            step = rf_slice.step

            if step is not None and step < 0 and stop is None:
                stop = -1

            l = float(stop - start)/float(step)
            self.assertEqual(
                int(math.ceil(l)),
                len(each_range[:])
            )


    def test_reformat_slices(self):
        with self.assertRaises(ValueError) as e:
            kenjutsu.reformat_slices(
                (slice(None), slice(None), Ellipsis), (1,)
            )

        self.assertEqual(
            str(e.exception),
            "Shape must be as large or larger than the number of slices"
            " without the Ellipsis."
        )

        with self.assertRaises(ValueError) as e:
            kenjutsu.reformat_slices(
                (Ellipsis, Ellipsis), (1,)
            )

        self.assertEqual(
            str(e.exception),
            "Only one Ellipsis is permitted. Found multiple."
        )

        rf_slice = kenjutsu.reformat_slices(slice(None))
        self.assertEqual(
            rf_slice,
            (slice(0, None, 1),)
        )

        rf_slice = kenjutsu.reformat_slices((slice(None),))
        self.assertEqual(
            rf_slice,
            (slice(0, None, 1),)
        )

        rf_slice = kenjutsu.reformat_slices(Ellipsis)
        self.assertEqual(
            rf_slice,
            (Ellipsis,)
        )

        rf_slice = kenjutsu.reformat_slices(Ellipsis, 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = kenjutsu.reformat_slices(tuple())
        self.assertEqual(
            rf_slice,
            (Ellipsis,)
        )

        rf_slice = kenjutsu.reformat_slices(tuple(), 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = kenjutsu.reformat_slices(slice(None), 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = kenjutsu.reformat_slices((slice(None),), 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = kenjutsu.reformat_slices((
            -1,
            slice(None),
            slice(3, None),
            slice(None, 5),
            slice(None, None, 2)
        ))
        self.assertEqual(
            rf_slice,
            (
                -1,
                slice(0, None, 1),
                slice(3, None, 1),
                slice(0, 5, 1),
                slice(0, None, 2)
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            (
                -1,
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2),
                [-1, -2, -1, 1, 5]
            ),
            (12, 10, 13, 15, 20, 10)
        )
        self.assertEqual(
            rf_slice,
            (
                11,
                slice(0, 10, 1),
                slice(3, 13, 1),
                slice(0, 5, 1),
                slice(0, 20, 2),
                [9, 8, 9, 1, 5]
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            Ellipsis,
            (2, 3, 4, 5)
        )
        self.assertEqual(
            rf_slice,
            (
                slice(0, 2, 1),
                slice(0, 3, 1),
                slice(0, 4, 1),
                slice(0, 5, 1)
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            (
                Ellipsis,
                slice(0, 1)
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            rf_slice,
            (
                slice(0, 2, 1),
                slice(0, 3, 1),
                slice(0, 4, 1),
                slice(0, 1, 1)
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            (
                slice(0, 1),
                Ellipsis
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            rf_slice,
            (
                slice(0, 1, 1),
                slice(0, 3, 1),
                slice(0, 4, 1),
                slice(0, 5, 1)
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            (
                slice(0, 1),
                Ellipsis,
                slice(0, 1)
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            rf_slice,
            (
                slice(0, 1, 1),
                slice(0, 3, 1),
                slice(0, 4, 1),
                slice(0, 1, 1)
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            (
                slice(0, 1),
                Ellipsis,
                slice(0, 1),
                slice(0, 1),
                slice(0, 1)
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            rf_slice,
            (
                slice(0, 1, 1),
                slice(0, 1, 1),
                slice(0, 1, 1),
                slice(0, 1, 1)
            )
        )


    def test_len_slice(self):
        with self.assertRaises(kenjutsu.UnknownSliceLengthException):
            kenjutsu.len_slice(slice(None))

        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)
            for start in itertools.chain([None], irange(-excess, excess)):
                for stop in itertools.chain([None], irange(-excess, excess)):
                    for step in itertools.chain(irange(-excess, excess)):
                        step = None if step == 0 else step

                        a_slice = slice(start, stop, step)

                        l = kenjutsu.len_slice(a_slice, size)
                        self.assertEqual(
                            l,
                            len(each_range[a_slice])
                        )

                        a_slice = list()
                        a_slice.append(0 if start is None else start)
                        a_slice.append(0 if stop is None else stop)
                        a_slice.append(0 if step is None else step)

                        a_op = operator.itemgetter(*a_slice)

                        expected_result = None
                        try:
                            expected_result = a_op(each_range)
                        except IndexError:
                            pass

                        if expected_result is not None:
                            l = kenjutsu.len_slice(a_slice, size)
                            self.assertEqual(len(expected_result), l)

                if start is not None:
                    a_slice = start

                    with self.assertRaises(TypeError):
                        kenjutsu.len_slice(a_slice, size)

            self.assertEqual(
                kenjutsu.len_slice(Ellipsis, size),
                len(each_range[:])
            )

            self.assertEqual(
                kenjutsu.len_slice(tuple(), size),
                len(each_range[:])
            )


    def test_len_slices(self):
        with self.assertRaises(kenjutsu.UnknownSliceLengthException):
            kenjutsu.len_slices((
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2)
            ))

        l = kenjutsu.len_slices(Ellipsis, 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = kenjutsu.len_slices(tuple(), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = kenjutsu.len_slices(slice(None), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = kenjutsu.len_slices((slice(None),), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = kenjutsu.len_slices(
            (
                -1,
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2),
                [-1, -2, -1, 1, 5]
            ),
            (12, 10, 13, 15, 20, 10)
        )
        self.assertEqual(
            l,
            (10, 10, 5, 10, 5)
        )

        l = kenjutsu.len_slices(
            Ellipsis,
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (2, 3, 4, 5)
        )

        l = kenjutsu.len_slices(
            (
                Ellipsis,
                slice(0, 1)
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (2, 3, 4, 1)
        )

        l = kenjutsu.len_slices(
            (
                slice(0, 1),
                Ellipsis
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (1, 3, 4, 5)
        )

        l = kenjutsu.len_slices(
            (
                slice(0, 1),
                Ellipsis,
                slice(0, 1)
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (1, 3, 4, 1)
        )

        l = kenjutsu.len_slices(
            (
                slice(0, 1),
                Ellipsis,
                slice(0, 1),
                slice(0, 1),
                slice(0, 1)
            ),
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (1, 1, 1, 1)
        )


    def test_split_blocks(self):
        with self.assertRaises(ValueError) as e:
            kenjutsu.split_blocks((1,), (1, 2), (1, 2, 3))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape`, `block_shape`, and `block_halo`"
            " should be the same."
        )

        with self.assertRaises(ValueError) as e:
            kenjutsu.split_blocks((1,), (1, 2))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape` and `block_shape` should be the"
            " same."
        )

        blocks = kenjutsu.split_blocks((2,), (1,))
        self.assertEqual(
            blocks,
            ([(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(0, 1, 1),)])
        )

        blocks = kenjutsu.split_blocks((2,), (-1,))
        self.assertEqual(
            blocks,
            ([(slice(0, 2, 1),)],
             [(slice(0, 2, 1),)],
             [(slice(0, 2, 1),)])
        )

        blocks = kenjutsu.split_blocks((2, 3,), (1, 1,))
        self.assertEqual(
            blocks,
            ([(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1))])
        )

        blocks = kenjutsu.split_blocks((2, 3,), (1, 1,), (0, 0))
        self.assertEqual(
            blocks,
            ([(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(1, 2, 1)),
              (slice(0, 1, 1), slice(2, 3, 1)),
              (slice(1, 2, 1), slice(0, 1, 1)),
              (slice(1, 2, 1), slice(1, 2, 1)),
              (slice(1, 2, 1), slice(2, 3, 1))],
             [(slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1)),
              (slice(0, 1, 1), slice(0, 1, 1))])
        )

        blocks = kenjutsu.split_blocks((10, 12,), (3, 2,), (4, 3,))
        self.assertEqual(
            blocks,
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
        )


    def tearDown(self):
        pass



if __name__ == '__main__':
    sys.exit(unittest.main())
