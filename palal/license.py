# -*- coding: utf-8 -*-

"""
    palal.license
    -------------

    This module is home to the `License` class.

    A License class has the meta-data associated with the license and the
    license text.

    It also defines a few utiliy functions that operate in licenses.

    :copyright: (c) 2015 by Ali Zaidi.
    :license: BSD, see LICENSE for more details.
"""

import os
import sys
import yaml


class License(object):
    """Holds license data as well as the functions that operate on it."""

    def __init__(self, text, delimiter='---'):
        """Load-up the given license text into a License object given the
        delimiter for YAML meta-data."""
        secs = text.split(delimiter)
        self.meta = yaml.load(secs[1])
        self.mkdn = ''.join(secs[2:])