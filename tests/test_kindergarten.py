#!/usr/bin/env python

"""Tests for `kindergarten` package."""


def test_import():
    from kindergarten import plot


def test_create_app():
    from kindergarten.core import Kindergarten

    Kindergarten(num_traces=5)


def test_qualitative_color_scales():
    from kindergarten.constants import QUALITATIVE_COLOR_SCALES

    assert len(QUALITATIVE_COLOR_SCALES) > 0


def test_no_params_without_implementation():
    from kindergarten.graph_options import params_without_implementation

    assert len(params_without_implementation) == 0
