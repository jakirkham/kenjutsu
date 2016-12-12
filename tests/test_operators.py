__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 16:20:14 GMT-0500$"


import doctest
import itertools
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
    def test_reverse_slice(self):
        # with self.assertRaises(ValueError) as e:
        #     format.reformat_slice(None)
        #
        # self.assertEqual(
        #     str(e.exception),
        #     "Expected a `slice` type. Instead got `None`."
        # )

        for size in [10, 11, 12]:
            excess = size + 3
            each_range = range(size)

            for start in itertools.chain([None], irange(-excess, excess)):
                for stop in itertools.chain([None],
                                            irange(-excess, excess)):
                    for step in itertools.chain(irange(-excess, excess)):
                        step = None if step == 0 else step

                        a_slice = slice(start, stop, step)

                        rv_slice = operators.reverse_slice(a_slice, size)
                        self.assertEqual(
                            each_range[a_slice][::-1],
                            each_range[rv_slice],
                            (a_slice, rv_slice)
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
                            rv_slice = operators.reverse_slice(a_slice, size)
                            rv_op = operator.itemgetter(*rv_slice)
                            self.assertEqual(
                                expected_result[::-1],
                                rv_op(each_range)
                            )
                        else:
                            with self.assertRaises(IndexError):
                                operators.reverse_slice(a_slice, size)

                if start is not None:
                    a_slice = start

                    expected_result = None
                    try:
                        expected_result = each_range[a_slice]
                    except IndexError:
                        pass

                    if expected_result is not None:
                        rv_slice = operators.reverse_slice(a_slice, size)
                        rv_op = operator.itemgetter(*rv_slice)
                        self.assertEqual(
                            expected_result[::-1],
                            rv_op(each_range)
                        )
                    else:
                        with self.assertRaises(IndexError):
                            operators.reverse_slice(a_slice, size)

            rv_slice = operators.reverse_slice(Ellipsis, size)
            self.assertEqual(
                each_range[::-1],
                each_range[rv_slice]
            )

            rv_slice = operators.reverse_slice(tuple(), size)
            self.assertEqual(
                each_range[::-1],
                each_range[rv_slice]
            )
