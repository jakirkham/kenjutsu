#!/usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 11:35:58 GMT-0500$"


import doctest
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
