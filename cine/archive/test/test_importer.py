"""
Tests for importer module
"""

import unittest

from .. import importer


def load_tests(loader, tests, pattern):
    "Build test suite for this module"
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(MovieImporterTest))
    return suite


class MovieImporterTest(unittest.TestCase):
    "MovieImporter tests"
    
    def test_clean_name(self):
        "Clean name functionality"
        i = importer.MovieImporter()
        # Excess white-space
        self.assertEqual(i.clean_name(
            '  Die Hard \n'), 
            'Die Hard')
        # Drop extension
        self.assertEqual(i.clean_name(
            'The Matrix.mp4'), 
            'The Matrix')
        # Drop extension
        self.assertEqual(i.clean_name(
            'Aliens.webm'), 
            'Aliens')       
        # Normalise format of year
        self.assertEqual(i.clean_name(
            'Wild at Heart [1990]'), 
            'Wild at Heart (1990)')

