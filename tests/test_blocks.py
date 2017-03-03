__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 15:26:16 GMT-0500$"


import doctest
import sys
import unittest

from kenjutsu import blocks


try:
    irange = xrange
except NameError:
    irange = range


# Load doctests from `blocks`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(blocks))
    return tests


class TestBlocks(unittest.TestCase):
    def setUp(self):
        pass


    def test_num_blocks(self):
        with self.assertRaises(ValueError) as e:
            blocks.num_blocks((1,), (1, 2))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape` and `block_shape` should be the"
            " same."
        )

        with self.assertRaises(ValueError) as e:
            blocks.num_blocks((1, 0), (1, -1))

        self.assertEqual(
            str(e.exception),
            "Shape of the space must all be positive definite."
            "Instead got: (1, 0)."
        )

        with self.assertRaises(ValueError) as e:
            blocks.num_blocks((1, 2), (1, 0))

        self.assertEqual(
            str(e.exception),
            "Shape of the blocks must all be positive or -1."
            "Instead got: (1, 0)."
        )

        with self.assertRaises(ValueError) as e:
            blocks.num_blocks((1, 2), (1, -2))

        self.assertEqual(
            str(e.exception),
            "Shape of the blocks must all be positive or -1."
            "Instead got: (1, -2)."
        )

        result = blocks.num_blocks((2,), (1,))
        self.assertEqual(
            result,
            (2,)
        )

        result = blocks.num_blocks((2,), (-1,))
        self.assertEqual(
            result,
            (1,)
        )

        result = blocks.num_blocks((2, 3), (1, 1,))
        self.assertEqual(
            result,
            (2, 3)
        )

        result = blocks.num_blocks((2, 3), (1, 2,))
        self.assertEqual(
            result,
            (2, 2)
        )

        result = blocks.num_blocks((10, 12), (3, 2,))
        self.assertEqual(
            result,
            (4, 6)
        )


    def test_split_blocks(self):
        with self.assertRaises(ValueError) as e:
            blocks.split_blocks((1,), (1, 2), (1, 2, 3))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape`, `block_shape`, and `block_halo`"
            " should be the same."
        )

        with self.assertRaises(ValueError) as e:
            blocks.split_blocks((1,), (1, 2))

        self.assertEqual(
            str(e.exception),
            "The dimensions of `space_shape` and `block_shape` should be the"
            " same."
        )

        with self.assertRaises(ValueError) as e:
            blocks.split_blocks((1, 0), (1, -1))

        self.assertEqual(
            str(e.exception),
            "Shape of the space must all be positive definite."
            "Instead got: (1, 0)."
        )

        with self.assertRaises(ValueError) as e:
            blocks.split_blocks((1, 2), (1, 0))

        self.assertEqual(
            str(e.exception),
            "Shape of the blocks must all be positive or -1."
            "Instead got: (1, 0)."
        )

        with self.assertRaises(ValueError) as e:
            blocks.split_blocks((1, 2), (1, -2))

        self.assertEqual(
            str(e.exception),
            "Shape of the blocks must all be positive or -1."
            "Instead got: (1, -2)."
        )

        with self.assertRaises(ValueError) as e:
            blocks.split_blocks((1, 2), (1, 1), (0, -1))

        self.assertEqual(
            str(e.exception),
            "Shape of the halo must all be positive semidefinite."
            "Instead got: (0, -1)."
        )

        result = blocks.split_blocks((2,), (1,))
        self.assertEqual(
            result,
            ([(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(0, 1, 1),)])
        )

        result = blocks.split_blocks((2,), (1,), index=True)
        self.assertEqual(
            result,
            ([(0,), (1,)],
             [(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(1, 2, 1),)],
             [(slice(0, 1, 1),), (slice(0, 1, 1),)])
        )

        result = blocks.split_blocks((2,), (-1,))
        self.assertEqual(
            result,
            ([(slice(0, 2, 1),)],
             [(slice(0, 2, 1),)],
             [(slice(0, 2, 1),)])
        )

        result = blocks.split_blocks((2, 3,), (1, 1,))
        self.assertEqual(
            result,
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

        result = blocks.split_blocks((2, 3,), (1, 1,), (0, 0))
        self.assertEqual(
            result,
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

        result = blocks.split_blocks((10, 12,), (3, 2,), (4, 3,))
        self.assertEqual(
            result,
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

        result = blocks.split_blocks((10, 12,), (3, 2,), (4, 3,), True)
        self.assertEqual(
            result,
            ([(0, 0),
              (0, 1),
              (0, 2),
              (0, 3),
              (0, 4),
              (0, 5),
              (1, 0),
              (1, 1),
              (1, 2),
              (1, 3),
              (1, 4),
              (1, 5),
              (2, 0),
              (2, 1),
              (2, 2),
              (2, 3),
              (2, 4),
              (2, 5),
              (3, 0),
              (3, 1),
              (3, 2),
              (3, 3),
              (3, 4),
              (3, 5)],
             [(slice(0, 3, 1), slice(0, 2, 1)),
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
