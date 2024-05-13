"""
Tests interface to collection file-structure.
"""

import doctest
import os
import unittest

from .. import collection


def load_tests(loader, tests, pattern):
    "Build test suite for this module"
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(CollectionGetFolderTest))
    suite.addTests(loader.loadTestsFromTestCase(CollectionCalculateFolderTest))
    suite.addTests(loader.loadTestsFromTestCase(CollectionTitlesTest))
    return suite


class CollectionGetFolderTest(unittest.TestCase):
    _data = os.path.join(os.path.dirname(__file__), 'data', 'clean')
    _data2 = os.path.join(os.path.dirname(__file__), 'data', 'clean2')

    def test_existing(self):
        "Existing titles found"
        c = collection.Collection(self._data, self._data2)
        # Under self._data root
        folder = c.get_folder('Curious George (2006)')
        self.assertTrue(os.path.isdir(folder))
        self.assertIn(self._data, folder)
        # Under self._data2 root
        folder = c.get_folder('Hot Rod (2007)')
        self.assertTrue(os.path.isdir(folder))
        self.assertIn(self._data2, folder)
        # Under 'Harry Potter' grouping folder, under self._data root
        folder = c.get_folder('Harry Potter and the Goblet of Fire (2005)')
        self.assertTrue(os.path.isdir(folder))
        self.assertIn(self._data, folder)
        self.assertIn('/Harry Potter/', folder)

    def test_missing(self):
        "Missing titles raise KeyError"
        c = collection.Collection(self._data, self._data2)
        with self.assertRaisesRegex(KeyError,
            "Title not found: 'Die Hard \(1988\)'"):
            folder = c.get_folder('Die Hard (1988)')

    def test_bad_title(self):
        c = collection.Collection(self._data, self._data2)
        with self.assertRaisesRegex(ValueError, "Title format error: 'Die Hard'"):
            folder = c.get_folder('Die Hard')

class CollectionCalculateFolderTest(unittest.TestCase):
    "Test the calculate_folder method"
    _data = os.path.join(os.path.dirname(__file__), 'data', 'clean')
    _data2 = os.path.join(os.path.dirname(__file__), 'data', 'clean2')

    def test_simple(self):
        "Simple case works as expected"
        c = collection.Collection(self._data)
        title = 'Die Hard (1988)'
        folder = c.calculate_folder(title)
        expected = os.path.join(self._data, title)
        self.assertEqual(folder, expected)

    def test_bad_title(self):
        "Title not in expected format raises ValueError"
        c = collection.Collection(self._data)
        with self.assertRaisesRegex(ValueError, "Title format error: 'Die Hard'"):
            folder = c.calculate_folder('Die Hard')

    def test_use_first_root(self):
        "When multiple roots present, first root is used"
        title = 'Die Hard (1988)'
        # Multiple roots
        c = collection.Collection(self._data, self._data2)
        folder = c.calculate_folder(title)
        expected = os.path.join(self._data, title)
        self.assertEqual(folder, expected)
        # Reverse order of roots
        c2 = collection.Collection(self._data2, self._data)
        folder2 = c2.calculate_folder(title)
        expected2 = os.path.join(self._data2, title)
        self.assertEqual(folder2, expected2)
        self.assertNotEqual(folder, folder2)

    def test_no_mkdir(self):
        "No folder is created as side-effect"
        title = 'Die Hard (1988)'
        c = collection.Collection(self._data)
        folder = c.calculate_folder(title)
        self.assertFalse(os.path.exists(folder))


class CollectionTitlesTest(unittest.TestCase):
    _data = os.path.join(os.path.dirname(__file__), 'data', 'clean')
    _data2 = os.path.join(os.path.dirname(__file__), 'data', 'clean2')

    def test_init_bad(self):
        "It is an error to create a collection without a root folder"
        # Single bad root
        with self.assertRaises(ValueError):
            c = collection.Collection('/no/such/folder/path')
        # One good root, one bad
        with self.assertRaises(ValueError):
            c = collection.Collection(self._data, '/just/plain/silly')

    def test_titles_count(self):
        "Number of titles found under root correct"
        c = collection.Collection(self._data)
        self.assertEqual(len(c.get_titles()), 12)

    def test_titles_count2(self):
        "Number of titles found under two roots correct"
        c = collection.Collection(self._data, self._data2)
        self.assertEqual(len(c.get_titles()), 16)

    def test_titles_keys(self):
        self.maxDiff = None
        "Names of titles found under root correct"
        c = collection.Collection(self._data)
        titles = sorted(c.get_titles().keys())
        self.assertEqual(titles, [
            'Curious George (2006)',
            'Dinosaur (2000)',
            'Harry Potter and the Chamber of Secrets (2002)',
            'Harry Potter and the Deathly Hallows - Part 1 (2010)',
            'Harry Potter and the Deathly Hallows - Part 2 (2011)',
            'Harry Potter and the Goblet of Fire (2005)',
            'Harry Potter and the Half-Blood Prince (2009)',
            'Harry Potter and the Order of the Phoenix (2007)',
            "Harry Potter and the Philosopher's Stone (2001)",
            'Harry Potter and the Prisoner of Azkaban (2004)',
            'How to Train Your Dragon (2010)',
            'Robocop (1987)'])

    def test_titles_keys2(self):
        "Names of titles found under two roots correct"
        c = collection.Collection(self._data, self._data2)
        titles = sorted(c.get_titles().keys())
        self.assertEqual(titles,
            ['Curious George (2006)',
            'Dinosaur (2000)',
            'Harry Potter and the Chamber of Secrets (2002)',
            'Harry Potter and the Deathly Hallows - Part 1 (2010)',
            'Harry Potter and the Deathly Hallows - Part 2 (2011)',
            'Harry Potter and the Goblet of Fire (2005)',
            'Harry Potter and the Half-Blood Prince (2009)',
            'Harry Potter and the Order of the Phoenix (2007)',
            "Harry Potter and the Philosopher's Stone (2001)",
            'Harry Potter and the Prisoner of Azkaban (2004)',
            'Hot Rod (2007)',
            'How to Train Your Dragon (2010)',
            'Robocop (1987)',
            'Scooby-Doo (2002)',
            'TRON (1982)',
            "The Sorcerer's Apprentice (2010)"])

    def test_titles_paths(self):
        "Paths found under roots are all files"
        c = collection.Collection(self._data, self._data2)
        titles = c.get_titles()
        for title in titles:
            path = titles[title]
            self.assertRegex(path, r'^/')
            self.assertTrue(os.path.isfile(path),
                "'{0}' is not a file".format(path))
