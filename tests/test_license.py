import os
import unittest

from palal import license


class TestLicense(unittest.TestCase):
    
    def setUp(self):
        """Load up all the licenses."""
        self.lics = []
        for ln in os.listdir(license.LIC_DIR):
            lp = os.path.join(license.LIC_DIR, ln)
            with open(lp) as lf:
                txt = lf.read()
                lic = license.License(txt)
                self.lics.append(lic)

    def test_license(self):
        """Check the licenses for key attrs."""
        lic_attrs = [
            'meta', 
            'mkdn'
        ]
        meta_attrs = [
            'title',
            'required',
            'permitted',
            'forbidden'
        ]
        for lic in self.lics:
            for la in lic_attrs:
                assert hasattr(lic, la)
                for ma in meta_attrs:
                    assert ma in lic.meta
