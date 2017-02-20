__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 14:20:52 GMT-0500$"


import doctest
import itertools
import math
import operator
import unittest

from kenjutsu import format


try:
    irange = xrange
except NameError:
    irange = range


# Load doctests from `format`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(format))
    return tests


class TestFormat(unittest.TestCase):
    def setUp(self):
        pass


    def test_index_to_slice(self):
        with self.assertRaises(TypeError) as e:
            format.index_to_slice(None)

        self.assertEqual(
            str(e.exception),
            "Expected an integral type. Instead got `None`."
        )

        with self.assertRaises(TypeError) as e:
            format.index_to_slice(2.5)

        self.assertEqual(
            str(e.exception),
            "Expected an integral type. Instead got `2.5`."
        )

        with self.assertRaises(TypeError) as e:
            format.index_to_slice((0,))

        self.assertEqual(
            str(e.exception),
            "Expected an integral type. Instead got `(0,)`."
        )

        with self.assertRaises(TypeError) as e:
            format.index_to_slice([0, 1])

        self.assertEqual(
            str(e.exception),
            "Expected an integral type. Instead got `[0, 1]`."
        )

        with self.assertRaises(TypeError) as e:
            format.index_to_slice(slice(None))

        self.assertEqual(
            str(e.exception),
            "Expected an integral type. Instead got `slice(None, None, None)`."
        )

        with self.assertRaises(TypeError) as e:
            format.index_to_slice(Ellipsis)

        self.assertEqual(
            str(e.exception),
            "Expected an integral type. Instead got `Ellipsis`."
        )

        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)

            for index in itertools.chain(irange(-excess, excess)):
                expected_result = []
                try:
                    expected_result = [each_range[index]]
                except IndexError:
                    pass

                rf_slice = format.index_to_slice(index)

                self.assertIsInstance(rf_slice, slice)

                result = list(each_range[rf_slice])
                self.assertEqual(result, expected_result)

                start = rf_slice.start
                stop = rf_slice.stop
                step = rf_slice.step

                self.assertEqual(int(math.copysign(1, index)), step)

                l = float(stop - start)/float(step)
                self.assertEqual(
                    int(math.ceil(l)),
                    1
                )


    def test_reformat_slice(self):
        with self.assertRaises(TypeError) as e:
            format.reformat_slice(None)

        self.assertEqual(
            str(e.exception),
            "Expected an index acceptable type."
            " Instead got, `None`."
        )

        with self.assertRaises(ValueError) as e:
            format.reformat_slice(slice(None, None, 0))

        self.assertEqual(
            str(e.exception),
            "Slice cannot have a step size of `0`."
        )

        with self.assertRaises(TypeError) as e:
            format.reformat_slice([None])

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

                        rf_slice = format.reformat_slice(a_slice)
                        self.assertEqual(
                            each_range[a_slice],
                            each_range[rf_slice]
                        )

                        rf_slice = format.reformat_slice(a_slice, size)
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
                            rf_slice = format.reformat_slice(a_slice)
                            rf_op = operator.itemgetter(*rf_slice)
                            self.assertEqual(
                                expected_result,
                                rf_op(each_range)
                            )

                            rf_slice = format.reformat_slice(a_slice, size)
                            rf_op = operator.itemgetter(*rf_slice)
                            self.assertEqual(
                                expected_result,
                                rf_op(each_range)
                            )
                        else:
                            format.reformat_slice(a_slice)
                            with self.assertRaises(IndexError):
                                format.reformat_slice(a_slice, size)

                if start is not None:
                    a_slice = start

                    expected_result = None
                    try:
                        expected_result = each_range[a_slice]
                    except IndexError:
                        pass

                    if expected_result is not None:
                        rf_slice = format.reformat_slice(a_slice)
                        self.assertEqual(
                            expected_result,
                            each_range[rf_slice]
                        )

                        rf_slice = format.reformat_slice(a_slice, size)
                        self.assertEqual(
                            expected_result,
                            each_range[rf_slice]
                        )
                    else:
                        format.reformat_slice(a_slice)
                        with self.assertRaises(IndexError):
                            format.reformat_slice(a_slice, size)

            rf_slice = format.reformat_slice(Ellipsis)
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            rf_slice = format.reformat_slice(Ellipsis, size)
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            rf_slice = format.reformat_slice(tuple())
            self.assertEqual(
                each_range[:],
                each_range[rf_slice]
            )

            rf_slice = format.reformat_slice(tuple(), size)
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
            format.reformat_slices(
                (slice(None), slice(None)), (1,)
            )

        self.assertEqual(
            str(e.exception),
            "Shape must be as large or larger than the number of slices."
        )

        with self.assertRaises(ValueError) as e:
            format.reformat_slices(
                (slice(None), slice(None), Ellipsis), (1,)
            )

        self.assertEqual(
            str(e.exception),
            "Shape must be as large or larger than the number of slices"
            " without the Ellipsis."
        )

        with self.assertRaises(ValueError) as e:
            format.reformat_slices(
                (Ellipsis, Ellipsis), (1,)
            )

        self.assertEqual(
            str(e.exception),
            "Only one Ellipsis is permitted. Found multiple."
        )

        with self.assertRaises(ValueError) as e:
            format.reformat_slices(
                ([0, 1], [0, 1]),
            )

        self.assertEqual(
            str(e.exception),
            "Only one integral sequence supported. Instead got `2`."
        )

        rf_slice = format.reformat_slices(slice(None))
        self.assertEqual(
            rf_slice,
            (slice(0, None, 1),)
        )

        rf_slice = format.reformat_slices((slice(None),))
        self.assertEqual(
            rf_slice,
            (slice(0, None, 1),)
        )

        rf_slice = format.reformat_slices(Ellipsis)
        self.assertEqual(
            rf_slice,
            (Ellipsis,)
        )

        rf_slice = format.reformat_slices(Ellipsis, 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = format.reformat_slices(tuple())
        self.assertEqual(
            rf_slice,
            (Ellipsis,)
        )

        rf_slice = format.reformat_slices(tuple(), 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = format.reformat_slices(slice(None), 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = format.reformat_slices(slice(None), (1, 2))
        self.assertEqual(
            rf_slice,
            (slice(0, 1, 1), slice(0, 2, 1))
        )

        rf_slice = format.reformat_slices((slice(None),), 10)
        self.assertEqual(
            rf_slice,
            (slice(0, 10, 1),)
        )

        rf_slice = format.reformat_slices((slice(None),), (1, 2))
        self.assertEqual(
            rf_slice,
            (slice(0, 1, 1), slice(0, 2, 1))
        )

        rf_slice = format.reformat_slices((
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

        rf_slice = format.reformat_slices(
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

        rf_slice = format.reformat_slices(
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

        rf_slice = format.reformat_slices(
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

        rf_slice = format.reformat_slices(
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

        rf_slice = format.reformat_slices(
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

        rf_slice = format.reformat_slices(
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


    def test_split_indices(self):
        with self.assertRaises(ValueError) as e:
            format.split_indices(
                ([0, 1], [0, 1]),
            )

        self.assertEqual(
            str(e.exception),
            "Only one integral sequence supported. Instead got `2`."
        )

        sp_slice = format.split_indices(
            (3, Ellipsis, 0, slice(2, 5, 1), -1)
        )
        self.assertEqual(
            sp_slice,
            [
                (3, Ellipsis, 0, slice(2, 5, 1), -1)
            ]
        )

        sp_slice = format.split_indices(
            (3, Ellipsis, 0, slice(2, 5, 1), [-1])
        )
        self.assertEqual(
            sp_slice,
            [
                (3, Ellipsis, 0, slice(2, 5, 1), slice(-1, -2, -1))
            ]
        )

        sp_slice = format.split_indices(
            (3, Ellipsis, [0], slice(2, 5, 1), -1)
        )
        self.assertEqual(
            sp_slice,
            [
                (3, Ellipsis, slice(0, 1, 1), slice(2, 5, 1), -1)
            ]
        )

        sp_slice = format.split_indices(
            (3, Ellipsis, [0, 1, 2], slice(2, 5, 1), -1)
        )
        self.assertEqual(
            sp_slice,
            [
                (3, Ellipsis, slice(0, 1, 1), slice(2, 5, 1), -1),
                (3, Ellipsis, slice(1, 2, 1), slice(2, 5, 1), -1),
                (3, Ellipsis, slice(2, 3, 1), slice(2, 5, 1), -1)
            ]
        )

        sp_slice = format.split_indices(
            (3, Ellipsis, [2, 0, 1, 2], slice(2, 5, 1), -1)
        )
        self.assertEqual(
            sp_slice,
            [
                (3, Ellipsis, slice(2, 3, 1), slice(2, 5, 1), -1),
                (3, Ellipsis, slice(0, 1, 1), slice(2, 5, 1), -1),
                (3, Ellipsis, slice(1, 2, 1), slice(2, 5, 1), -1),
                (3, Ellipsis, slice(2, 3, 1), slice(2, 5, 1), -1)
            ]
        )
