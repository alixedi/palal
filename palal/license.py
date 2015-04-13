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

DIR = os.path.dirname(os.path.realpath(__file__))
LIC_DIR = os.path.join(DIR, '_licenses')

class License(object):
    """Holds license data as well as the functions that operate on it."""

    def __init__(self, text, delimiter='---'):
        """Load-up the given license text into a License object given the
        delimiter for YAML meta-data."""
        secs = text.split(delimiter)
        self.meta = yaml.load(secs[1])
        self.mkdn = ''.join(secs[2:])

    def get_vector(self, max_choice=3):
        """Return pseudo-choice vectors."""
        vec = {}
        for dim in ['forbidden', 'required', 'permitted']:
            if self.meta[dim] is None:
                continue
            dim_vec = map(lambda x: (x, max_choice), self.meta[dim])
            vec[dim] = dict(dim_vec)
        return vec


def license_loader(lic_dir=LIC_DIR):
    """Loads licenses from the given directory."""
    lics = []
    for ln in os.listdir(lic_dir):
        lp = os.path.join(lic_dir, ln)
        with open(lp) as lf:
            txt = lf.read()
            lic = License(txt)
            lics.append(lic)
    return lics