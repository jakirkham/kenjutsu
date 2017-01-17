#!/usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 14:49:29 GMT-0500$"


import doctest
import itertools
import operator
import sys
import unittest

from kenjutsu import measure


try:
    irange = xrange
except NameError:
    irange = range


# Load doctests from `measure`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(measure))
    return tests


class TestMeasure(unittest.TestCase):
    def setUp(self):
        pass


    def test_len_slice(self):
        with self.assertRaises(measure.UnknownSliceLengthException):
            measure.len_slice(slice(None))

        with self.assertRaises(measure.UnknownSliceLengthException):
            measure.len_slice(slice(0, -1, 1))

        with self.assertRaises(measure.UnknownSliceLengthException):
            measure.len_slice(slice(None, None, -1))

        with self.assertRaises(measure.UnknownSliceLengthException):
            measure.len_slice(slice(-1, 1, -1))

        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)
            for start in itertools.chain([None], irange(-excess, excess)):
                for stop in itertools.chain([None], irange(-excess, excess)):
                    for step in itertools.chain(irange(-excess, excess)):
                        step = None if step == 0 else step

                        a_slice = slice(start, stop, step)

                        l = measure.len_slice(a_slice, size)
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
                            l = measure.len_slice(a_slice, size)
                            self.assertEqual(len(expected_result), l)

                if start is not None:
                    a_slice = start

                    with self.assertRaises(TypeError):
                        measure.len_slice(a_slice, size)

            self.assertEqual(
                measure.len_slice(Ellipsis, size),
                len(each_range[:])
            )

            self.assertEqual(
                measure.len_slice(tuple(), size),
                len(each_range[:])
            )


    def test_len_slices(self):
        with self.assertRaises(measure.UnknownSliceLengthException):
            measure.len_slices((
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2)
            ))

        l = measure.len_slices(Ellipsis, 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = measure.len_slices(tuple(), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = measure.len_slices(slice(None), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = measure.len_slices((slice(None),), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = measure.len_slices(
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

        l = measure.len_slices(
            Ellipsis,
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (2, 3, 4, 5)
        )

        l = measure.len_slices(
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

        l = measure.len_slices(
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

        l = measure.len_slices(
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

        l = measure.len_slices(
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


    def tearDown(self):
        pass



if __name__ == '__main__':
    sys.exit(unittest.main())
