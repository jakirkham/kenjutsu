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


if __name__ == '__main__':
    sys.exit(unittest.main())
