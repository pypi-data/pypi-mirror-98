# -*- coding: utf-8 -*-
# This file is part of the markdown_aafigure project
# https://gitlab.com/mbarkhau/markdown_aafigure
#
# Copyright (c) 2018-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__version__ = 'v202103.1010'
from markdown_aafigure.extension import AafigureExtension


def _make_extension(**kwargs):
    return AafigureExtension(**kwargs)


makeExtension = _make_extension
__all__ = ['makeExtension', '__version__']
