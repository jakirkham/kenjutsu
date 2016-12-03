#!/usr/bin/env python

# -*- coding: utf-8 -*-


import doctest
import sys
import unittest

from kenjutsu import kenjutsu


# Load doctests from `kenjutsu`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(kenjutsu))
    return tests


class TestKenjutsu(unittest.TestCase):
    def setUp(self):
        pass


    def test_reformat_slice(self):
        rf_slice = kenjutsu.reformat_slice(slice(None))
        self.assertEqual(
            rf_slice,
            slice(0, None, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(None), 10)
        self.assertEqual(
            rf_slice,
            slice(0, 10, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None))
        self.assertEqual(
            rf_slice,
            slice(2, None, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None), 10)
        self.assertEqual(
            rf_slice,
            slice(2, 10, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None, None))
        self.assertEqual(
            rf_slice,
            slice(2, None, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None, None), 10)
        self.assertEqual(
            rf_slice,
            slice(2, 10, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -1))
        self.assertEqual(
            rf_slice,
            slice(2, -1, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -1), 10)
        self.assertEqual(
            rf_slice,
            slice(2, 9, 1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, -1))
        self.assertEqual(
            rf_slice,
            slice(-1, None, -1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, -1), 10)
        self.assertEqual(
            rf_slice,
            slice(9, None, -1)
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, -20), 10)
        self.assertEqual(
            rf_slice,
            slice(9, None, -10)
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, 20), 10)
        self.assertEqual(
            rf_slice,
            slice(0, 10, 10)
        )

        rf_slice = kenjutsu.reformat_slice(slice(-15, None, -20), 10)
        self.assertEqual(
            rf_slice,
            slice(0, 0, -10)
        )

        rf_slice = kenjutsu.reformat_slice(slice(None))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, 2))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, 6))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:6]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, 6, 3))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:6:3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -6, 3))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:-6:3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None, 3))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2::3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -1))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, 20))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -20))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:-20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(20, -1))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[20:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(-20, -1))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[-20:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(-5, -1))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[-5:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, -1))
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[::-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, 2), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, 6), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:6]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, 6, 3), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:6:3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -6, 3), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:-6:3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, None, 3), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2::3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -1), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, 20), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(2, -20), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[2:-20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(20, -1), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[20:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(-20, -1), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[-20:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(-5, -1), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[-5:-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, -1), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[::-1]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, -20), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[::-20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, None, 20), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[::20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(-15, None, -20), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[-15::-20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(15, None, -20), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[15::-20]
        )

        rf_slice = kenjutsu.reformat_slice(slice(-5, None, -2), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[-5::-2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, -5, -2), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:-5:-2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, -15, -2), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:-15:-2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, 15, -2), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:15:-2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(None, -3, 2), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[:-3:2]
        )

        rf_slice = kenjutsu.reformat_slice(slice(5, 3, None), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[5:3]
        )

        rf_slice = kenjutsu.reformat_slice(slice(3, 5, -1), 10)
        self.assertEqual(
            range(10)[rf_slice],
            range(10)[3:5:-1]
        )


    def test_reformat_slices(self):
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
            slice(None),
            slice(3, None),
            slice(None, 5),
            slice(None, None, 2)
        ))
        self.assertEqual(
            rf_slice,
            (
                slice(0, None, 1),
                slice(3, None, 1),
                slice(0, 5, 1),
                slice(0, None, 2)
            )
        )

        rf_slice = kenjutsu.reformat_slices(
            (
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2)
            ),
            (10, 13, 15, 20)
        )
        self.assertEqual(
            rf_slice,
            (
                slice(0, 10, 1),
                slice(3, 13, 1),
                slice(0, 5, 1),
                slice(0, 20, 2)
            )
        )


    def test_len_slice(self):
        with self.assertRaises(kenjutsu.UnknownSliceLengthException):
            kenjutsu.len_slice(slice(None))

        l = kenjutsu.len_slice(slice(None), 10)
        self.assertEqual(l, 10)

        l = kenjutsu.len_slice(slice(None), 10)
        self.assertEqual(l, len(range(10)[:]))

        l = kenjutsu.len_slice(slice(None, None, -1), 10)
        self.assertEqual(l, 10)

        l = kenjutsu.len_slice(slice(None, None, -1), 10)
        self.assertEqual(l, len(range(10)[::-1]))

        l = kenjutsu.len_slice(slice(None, None, 20), 10)
        self.assertEqual(l, 1)

        l = kenjutsu.len_slice(slice(None, None, 20), 10)
        self.assertEqual(l, len(range(10)[::20]))

        l = kenjutsu.len_slice(slice(None, None, -20), 10)
        self.assertEqual(l, 1)

        l = kenjutsu.len_slice(slice(None, None, -20), 10)
        self.assertEqual(l, len(range(10)[::-20]))

        l = kenjutsu.len_slice(slice(-15, None, -20), 10)
        self.assertEqual(l, 0)

        l = kenjutsu.len_slice(slice(-15, None, -20), 10)
        self.assertEqual(l, len(range(10)[-15::-20]))

        l = kenjutsu.len_slice(slice(15, None, -20), 10)
        self.assertEqual(l, 1)

        l = kenjutsu.len_slice(slice(15, None, -20), 10)
        self.assertEqual(l, len(range(10)[15::-20]))

        l = kenjutsu.len_slice(slice(2, None), 10)
        self.assertEqual(l, 8)

        l = kenjutsu.len_slice(slice(2, None), 10)
        self.assertEqual(l, len(range(10)[2:]))

        l = kenjutsu.len_slice(slice(2, None, None), 10)
        self.assertEqual(l, 8)

        l = kenjutsu.len_slice(slice(2, None, None), 10)
        self.assertEqual(l, len(range(10)[2:]))

        l = kenjutsu.len_slice(slice(2, 6))
        self.assertEqual(l, 4)

        l = kenjutsu.len_slice(slice(2, 6), 10)
        self.assertEqual(l, 4)

        l = kenjutsu.len_slice(slice(2, 6), 1000)
        self.assertEqual(l, 4)

        l = kenjutsu.len_slice(slice(2, 6), 10)
        self.assertEqual(l, len(range(10)[2:6]))

        l = kenjutsu.len_slice(slice(2, 6, 3))
        self.assertEqual(l, 2)

        l = kenjutsu.len_slice(slice(2, 6, 3))
        self.assertEqual(l, len(range(10)[2:6:3]))

        l = kenjutsu.len_slice(slice(-5, None, -2), 10)
        self.assertEqual(l, 3)

        l = kenjutsu.len_slice(slice(-5, None, -2), 10)
        self.assertEqual(l, len(range(10)[-5::-2]))

        # TODO: Fix so it works.
        l = kenjutsu.len_slice(slice(None, -5, -2), 10)
        self.assertEqual(l, 2)

        l = kenjutsu.len_slice(slice(None, -5, -2), 10)
        self.assertEqual(l, len(range(10)[:-5:-2]))

        l = kenjutsu.len_slice(slice(None, -15, -2), 10)
        self.assertEqual(l, 5)

        l = kenjutsu.len_slice(slice(None, -15, -2), 10)
        self.assertEqual(l, len(range(10)[:-15:-2]))

        l = kenjutsu.len_slice(slice(None, 15, -2), 10)
        self.assertEqual(l, 0)

        l = kenjutsu.len_slice(slice(None, 15, -2), 10)
        self.assertEqual(l, len(range(10)[:15:-2]))

        l = kenjutsu.len_slice(slice(None, -3, 2), 10)
        self.assertEqual(l, 4)

        l = kenjutsu.len_slice(slice(None, -3, 2), 10)
        self.assertEqual(l, len(range(10)[:-3:2]))


    def test_len_slices(self):
        with self.assertRaises(kenjutsu.UnknownSliceLengthException):
            kenjutsu.len_slices((
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2)
            ))

        l = kenjutsu.len_slices(
            (
                slice(None),
                slice(3, None),
                slice(None, 5),
                slice(None, None, 2)
            ),
            (10, 13, 15, 20)
        )
        self.assertEqual(
            l,
            (10, 10, 5, 10)
        )


    def test_split_blocks(self):
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
