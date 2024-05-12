
import sqlite3
from unittest import TestCase

from cine.database import Database
from cine.tables import AKAs, Episodes, Names, Principals, Ratings, Titles

from . import data as samples


class DBTestCase(TestCase):
    db: Database

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.db = Database()


class DatabaseTest(DBTestCase):
    """
    The database file and top-level interface to its data.
    """
    def test_init(self) -> None:
        # Database
        self.assertIsInstance(self.db, Database)

        # Tables
        self.assertIsInstance(self.db.akas, AKAs)
        self.assertIsInstance(self.db.episodes, Episodes)
        self.assertIsInstance(self.db.names, Names)
        self.assertIsInstance(self.db.principals, Principals)
        self.assertIsInstance(self.db.ratings, Ratings)
        self.assertIsInstance(self.db.titles, Titles)

    def test_cursor(self) -> None:
        self.assertIsInstance(self.db.cursor(), sqlite3.Cursor)

    def test_get_table_names(self) -> None:
        names = self.db.get_table_names()
        expected = [
            'akas', 'episodes', 'names', 'principals', 'ratings', 'titles',
        ]
        self.assertEqual(names, expected)


# Tables ###################################################

class AKAsTest(DBTestCase):
    def test_akas_insert_and_select(self) -> None:
        # Insert
        akas = self.db.akas
        self.assertIsInstance(akas, AKAs)
        self.assertEqual(akas.count(), 0)
        pk = akas.insert(samples.title_akas)
        self.assertEqual(pk, 1)
        self.assertEqual(akas.count(), 1)

        # Select
        data = akas.select(pk)
        expected = {
            'title_id': 'tt0000084',
            'ordering': 1,
            'title': 'The Drunkards',
            'region': 'GB',
            'language': None,
            'is_original_title': 0
        }
        self.assertEqual(data, expected)


class EpisodesTest(DBTestCase):
    def test_episodes_insert_and_select(self) -> None:
        # Insert
        episodes = self.db.episodes
        self.assertIsInstance(episodes, Episodes)
        self.assertEqual(episodes.count(), 0)
        pk = episodes.insert(samples.title_episodes)
        self.assertEqual(pk, 1)
        self.assertEqual(episodes.count(), 1)

        # Select
        data = episodes.select(pk)
        expected = {
            'tconst': 'tt0078459',
            'parent': 'tt0159876',
            'season': 6,
            'episode': 5,
        }
        self.assertEqual(data, expected)


class NamesTest(DBTestCase):
    """
    The names, births, and deaths of over 11 million people.
    """
    def test_names_insert_and_select(self) -> None:
        # Insert
        names = self.db.names
        self.assertIsInstance(names, Names)
        self.assertEqual(names.count(), 0)
        pk = names.insert(samples.name_basics)
        self.assertEqual(pk, 1)
        self.assertEqual(names.count(), 1)

        # Select
        data = names.select(pk)
        expected = {
            'birth_year': 1919,
            'death_year': 2006,
            'nconst': 'nm0000999',
            'primary_name': 'Red Buttons',
        }
        self.assertEqual(data, expected)


class PrincipalsTest(DBTestCase):
    def test_principals_insert_and_select(self) -> None:
        # Insert
        principals = self.db.principals
        self.assertIsInstance(principals, Principals)
        self.assertEqual(principals.count(), 0)
        pk = principals.insert(samples.title_principals)
        self.assertEqual(pk, 1)
        self.assertEqual(principals.count(), 1)

        # Select
        data = principals.select(pk)
        expected = {
            'tconst': 'tt0000109',
            'ordering': 4,
            'nconst': 'nm0005658',
            'category': 'cinematographer',
            'job': None,
            'characters': None,
        }
        self.assertEqual(data, expected)


class RatingsTest(DBTestCase):
    def test_ratings_insert_and_select(self) -> None:
        # Insert
        ratings = self.db.ratings
        self.assertIsInstance(ratings, Ratings)
        self.assertEqual(ratings.count(), 0)
        pk = ratings.insert(samples.title_ratings)
        self.assertEqual(pk, 1)
        self.assertEqual(ratings.count(), 1)

        # Select
        data = ratings.select(pk)
        expected = {
            'tconst': 'tt0000001',
            'average_rating': 4.5,
            'num_votes': 466,
        }
        self.assertEqual(data, expected)


class TitlesTest(DBTestCase):
    """
    Basic info for a title.
    """
    def test_titles_insert_and_select(self) -> None:
        # Insert
        titles = self.db.titles
        self.assertIsInstance(titles, Titles)
        self.assertEqual(titles.count(), 0)
        pk = titles.insert(samples.title_basics)
        self.assertEqual(pk, 1)
        self.assertEqual(titles.count(), 1)

        # Select
        data = titles.select(pk)
        expected = {
            'tconst': 'tt0000831',
            'title_type': 'short',
            'primary_title': 'The Cord of Life',
            'original_title': 'The Cord of Life',
            'is_adult': 0,
            'start_year': 1909,
            'end_year': None,
            'runtime_minutes': 9,
        }
        self.assertEqual(data, expected)
