
import unittest

from .. import util


def load_tests(loader, tests, pattern):
    "Build test suite for this module"
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(UtilTest))
    return suite



class TestGuessType(TestCase):
    """
    Test Movie Model guessing type.
    """
    def test_movie(self):
        self.assertEqual(utils.guess_type(
            'Die Hard (1988)'), 'movie')

    def test_tv_movie(self):
        self.assertEqual(utils.guess_type(
            "A Midsummer Night's Dream (2005) (TV)"), 'straight-to-tv')

    def test_dvd_movie(self):
        self.assertEqual(utils.guess_type(
            "A Midsummer Night's Dream (2005) (TV)"), 'straight-to-tv')

    def test_tv_series(self):
        self.assertEqual(utils.guess_type(
            "A Midsummer Night's Dream (2005) (TV)"), 'straight-to-tv')


class TestUncommaName(TestCase):
    def test_uncomma(self):
        self.assertEqual(utils.uncomma_name('Matthews, Leon'), 'Leon Matthews')
        self.assertEqual(utils.uncomma_name('Mr. T'), 'Mr. T')


class TestExtractYear(TestCase):
    def test_simple(self):
        """
        Simple examples work as expected.
        """
        self.assertEqual(utils.extract_year('Die Hard (1988)'), 1988)
        self.assertEqual(utils.extract_year('MacGruber (2010)'), 2010)

    def test_multiple_years(self):
        """
        Titles with multiple years do not cause confusion.
        """
        self.assertEqual(utils.extract_year(
            '1984 (1956)'), 1956)
        self.assertEqual(utils.extract_year(
            '"EastEnders" (1985) {(2000-09-25)}'), 1985)
        self.assertEqual(utils.extract_year(
            '"South Park" (1997) {Timmy 2000 (#4.3)}'), 1997)

    def test_disambiguation(self):
        """
        Titles disambiguated for uniqueness do not cause confusion.
        """
        self.assertEqual(utils.extract_year('Red (2009/I)'), 2009)
        self.assertEqual(utils.extract_year('Red (2009/II)'), 2009)
        self.assertEqual(utils.extract_year('Red (2009/III)'), 2009)
        self.assertEqual(utils.extract_year('Red (2009/IV)'), 2009)
        self.assertEqual(utils.extract_year('Red (2009/V)'), 2009)
        self.assertEqual(utils.extract_year('Red (2009/VI)'), 2009)


class UtilTest(unittest.TestCase):

    def test_clean_title_bad(self):
        "ValueError raised if title in bad format"
        with self.assertRaises(ValueError): util.clean_title('')
        with self.assertRaises(ValueError): util.clean_title(' ')
        with self.assertRaises(ValueError): util.clean_title('(2011)')
        with self.assertRaises(ValueError): util.clean_title('  (2011)')
        with self.assertRaises(ValueError): util.clean_title('(2011)  ')
        with self.assertRaises(ValueError): util.clean_title('about.mpg')
        with self.assertRaises(ValueError): util.clean_title('cine.xml')
        with self.assertRaises(ValueError): util.clean_title('folder.jpg')
        with self.assertRaises(ValueError): util.clean_title('be-cool-extras-010.ogm')
        with self.assertRaises(ValueError): util.clean_title('blah-blah.nfo')
        with self.assertRaises(ValueError): util.clean_title('subtitles.srt')

    def test_clean_title_bad_regressions(self):
        "Bad names found in the wild shouldn't bother us again"
        with self.assertRaises(ValueError):
            util.clean_title('._Babylon A.D. (2008)')

    def test_clean_title_good(self):
        "Title returned in canonical IMDB format, without unwanted extras"
        self.assertEqual(util.clean_title(
            ' Robocop (1987).webm   '),
            'Robocop (1987)')
        self.assertEqual(util.clean_title(
            'Big (1988).ogm'),
            'Big (1988)')
        self.assertEqual(util.clean_title(
            'Curious George (2006).mkv'),
            'Curious George (2006)')
        self.assertEqual(util.clean_title(
            '08. Harry Potter and the Deathly Hallows - Part 2 (2011).mp4'),
            'Harry Potter and the Deathly Hallows - Part 2 (2011)')
