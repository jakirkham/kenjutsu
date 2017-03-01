__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 16:20:14 GMT-0500$"


import doctest
import itertools
import math
import operator
import unittest

from kenjutsu import operators


try:
    irange = xrange
except NameError:
    irange = range


# Load doctests from `operators`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(operators))
    return tests


class TestOperators(unittest.TestCase):
    def setUp(self):
        pass


    def test_reformat_slice(self):
        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)

            for start_1, start_2 in itertools.product(*itertools.tee(
                    itertools.chain([None], irange(-excess, excess)))):
                for stop_1, stop_2 in itertools.product(*itertools.tee(
                        itertools.chain([None], irange(-excess, excess)))):
                    for step_1, step_2 in itertools.product(*itertools.tee(
                            irange(-excess, excess))):
                        step_1 = None if step_1 == 0 else step_1
                        step_2 = None if step_2 == 0 else step_2

                        slice_1 = slice(start_1, stop_1, step_1)
                        slice_2 = slice(start_2, stop_2, step_2)

                        j_slice = operators.join_slice(slice_1, slice_2)
                        print((slice_1, slice_2, j_slice))
                        self.assertEqual(
                            each_range[slice_1][slice_2],
                            each_range[j_slice]
                        )

                        j_slice = operators.join_slice(slice_1, slice_2, size)
                        self.assertEqual(
                            each_range[slice_1][slice_2],
                            each_range[j_slice]
                        )

                        new_start = j_slice.start
                        new_stop = j_slice.stop
                        new_step = j_slice.step

                        if (new_step is not None and
                            new_step < 0 and
                            new_stop is None):
                            new_stop = -1

                        l = float(new_stop - new_start)/float(new_step)
                        self.assertEqual(
                            int(math.ceil(l)),
                            len(each_range[slice_1][slice_2])
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
                            rf_slice = operators.reformat_slice(a_slice)
                            rf_op = operator.itemgetter(*rf_slice)
                            self.assertEqual(
                                expected_result,
                                rf_op(each_range)
                            )

                            rf_slice = operators.reformat_slice(a_slice, size)
                            rf_op = operator.itemgetter(*rf_slice)
                            self.assertEqual(
                                expected_result,
                                rf_op(each_range)
                            )
                        else:
                            operators.reformat_slice(a_slice)
                            with self.assertRaises(IndexError):
                                operators.reformat_slice(a_slice, size)

                if start is not None:
                    a_slice = start

                    expected_result = None
                    try:
                        expected_result = each_range[a_slice]
                    except IndexError:
                        pass

                    if expected_result is not None:
                        rf_slice = operators.reformat_slice(a_slice)
                        self.assertEqual(
                            expected_result,
                            each_range[rf_slice]
                        )

                        rf_slice = operators.reformat_slice(a_slice, size)
                        self.assertEqual(
                            expected_result,
                            each_range[rf_slice]
                        )
                    else:
                        operators.reformat_slice(a_slice)
                        with self.assertRaises(IndexError):
                            operators.reformat_slice(a_slice, size)
