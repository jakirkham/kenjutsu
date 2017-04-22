__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 16:20:14 GMT-0500$"


import doctest
import unittest

from kenjutsu import operators


# Load doctests from `operators`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(operators))
    return tests


class TestOperators(unittest.TestCase):
    def test_split_multindex(self):
        pass
