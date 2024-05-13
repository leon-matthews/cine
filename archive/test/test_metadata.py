
import unittest

from .. import collection


def load_tests(loader, tests, pattern):
    "Build test suite for this module"
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(MetadataTest))
    return suite


class MetadataTest(unittest.TestCase):
    def test_metadata(self):
        self.assertTrue(True)
