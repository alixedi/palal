import unittest
import subprocess
import palal


class TestSimple(unittest.TestCase):
    
    def test_cli(self):
        subprocess.check_call(['palal --h'], shell=True)
