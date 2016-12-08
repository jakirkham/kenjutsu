# -*- coding: utf-8 -*-

"""
The module ``core`` provides support for working with ``slice``\ s.

===============================================================================
Overview
===============================================================================
The module ``core`` provides several functions that are useful for working
with a Python ``slice`` or ``tuple`` of ``slice``\ s. This is of particular
value when working with NumPy_.

.. _NumPy: http://www.numpy.org/

===============================================================================
API
===============================================================================
"""


from __future__ import absolute_import


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 11:35:58 GMT-0500$"


import kenjutsu.blocks
import kenjutsu.format
import kenjutsu.measure


reformat_slice = kenjutsu.format.reformat_slice
reformat_slices = kenjutsu.format.reformat_slices

UnknownSliceLengthException = kenjutsu.measure.UnknownSliceLengthException
len_slice = kenjutsu.measure.len_slice
len_slices = kenjutsu.measure.len_slices

split_blocks = kenjutsu.blocks.split_blocks
