#!/usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 11:35:58 GMT-0500$"


import doctest
import itertools
import operator
import sys
import unittest

from kenjutsu import core


try:
    irange = xrange
except NameError:
    irange = range


# Load doctests from `core`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(core))
    return tests


class TestCore(unittest.TestCase):
    def setUp(self):
        pass


    def test_len_slice(self):
        with self.assertRaises(core.UnknownSliceLengthException):
            core.len_slice(slice(None))

        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)
            for start in itertools.chain([None], irange(-excess, excess)):
                for stop in itertools.chain([None], irange(-excess, excess)):
                    for step in itertools.chain(irange(-excess, excess)):
                        step = None if step == 0 else step

                        a_slice = slice(start, stop, step)

                        l = core.len_slice(a_slice, size)
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
                            l = core.len_slice(a_slice, size)
                            self.assertEqual(len(expected_result), l)

                if start is not None:
                    a_slice = start

                    with self.assertRaises(TypeError):
                        core.len_slice(a_slice, size)

            self.assertEqual(
                core.len_slice(Ellipsis, size),
                len(each_range[:])
            )

            self.assertEqual(
                core.len_slice(tuple(), size),
                len(each_range[:])
            )


    def test_len_slices(self):
        with self.assertRaises(core.UnknownSliceLengthException):
            core.len_slices((
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2)
            ))

        l = core.len_slices(Ellipsis, 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = core.len_slices(tuple(), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = core.len_slices(slice(None), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = core.len_slices((slice(None),), 10)
        self.assertEqual(
            l,
            (10,)
        )

        l = core.len_slices(
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

        l = core.len_slices(
            Ellipsis,
            (2, 3, 4, 5)
        )
        self.assertEqual(
            l,
            (2, 3, 4, 5)
        )

        l = core.len_slices(
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

        l = core.len_slices(
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

        l = core.len_slices(
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

        l = core.len_slices(
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
            core.split_blocks((1,), (1, 2), (1, 2, 3))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape`, `block_shape`, and `block_halo`"
            " should be the same."
        )

        with self.assertRaises(ValueError) as e:
            core.split_blocks((1,), (1, 2))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape` and `block_shape` should be the"
            " same."
        )

        blocks = core.split_blocks((2,), (1,))
        self.assertEqual(
            blocks,
            ([(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(0, 1, 1),)])
        )

        blocks = core.split_blocks((2,), (-1,))
        self.assertEqual(
            blocks,
            ([(slice(0, 2, 1),)],
             [(slice(0, 2, 1),)],
             [(slice(0, 2, 1),)])
        )

        blocks = core.split_blocks((2, 3,), (1, 1,))
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

        blocks = core.split_blocks((2, 3,), (1, 1,), (0, 0))
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

        blocks = core.split_blocks((10, 12,), (3, 2,), (4, 3,))
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
