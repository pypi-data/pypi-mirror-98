# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2018, 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA-DB tests."""

from __future__ import absolute_import, print_function


def test_version():
    """Test version import."""
    from reana_db import __version__

    assert __version__
