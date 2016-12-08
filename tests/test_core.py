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


    def tearDown(self):
        pass



if __name__ == '__main__':
    sys.exit(unittest.main())
