
from unittest import TestCase

from cine import readers

from . import DATA_FOLDER, NUM_SAMPLE_ROWS
from . import data as samples


class BaseTest(TestCase):
    def test_from_strings_not_implemented(self) -> None:
        record = readers.Record()
        message = r"^Sub-classes require from_strings\(\) method$"
        with self.assertRaisesRegex(NotImplementedError, message):
            record.from_strings('')



class NameBasicsTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.name_basics.as_dict()
        expected = {
            'nconst': 'nm0000999',
            'primary_name': 'Red Buttons',
            'birth_year': 1919,
            'death_year': 2006,
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.NameBasics.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.NameBasics)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

        # Last record
        expected = readers.NameBasics(
            nconst='nm9993719',
            primary_name='Andre Hill',
            birth_year=None,
            death_year=None,
            primary_profession=['writer'],
            known_for_titles=[],
        )
        self.assertEqual(obj, expected)

    def test_from_strings(self) -> None:
        obj = readers.NameBasics.from_strings(samples.name_basics_strings)
        self.assertEqual(obj.nconst, 'nm0000999')
        self.assertEqual(obj.primary_name, 'Red Buttons')
        self.assertEqual(obj.birth_year, 1919)
        self.assertEqual(obj.death_year, 2006)
        self.assertEqual(
            obj.primary_profession,
            ['actor', 'soundtrack', 'miscellaneous'],
        )
        self.assertEqual(
            obj.known_for_titles,
            ['tt0076538', 'tt0069113', 'tt0056197', 'tt0050933'],
        )

    def test_from_strings_optional(self) -> None:
        obj = readers.NameBasics.from_strings(samples.name_basics_strings2)
        self.assertEqual(obj.nconst, 'nm0000998')
        self.assertEqual(obj.primary_name, 'Jake Busey')
        self.assertEqual(obj.birth_year, 1971)
        self.assertEqual(obj.death_year, None)
        self.assertEqual(
            obj.primary_profession,
            ['actor', 'producer', 'music_department'],
        )
        self.assertEqual(
            obj.known_for_titles,
            ['tt0120201', 'tt0116365', 'tt0120660', 'tt3829266'],
        )


class TitleAkasTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.title_akas.as_dict()
        expected = {
            'title_id': 'tt0000084',
            'ordering': 1,
            'title': 'The Drunkards',
            'region': 'GB',
            'language': None,
            'is_original_title': False,
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.TitleAkas.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitleAkas)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

        # Last record
        expected = readers.TitleAkas(
            title_id='tt9916880',
            ordering=1,
            title='Horrid Henry Knows It All',
            region=None,
            language=None,
            types=['original'],
            attributes=None,
            is_original_title=True,
        )
        self.assertEqual(expected, obj)

    def test_from_strings(self) -> None:
        obj = readers.TitleAkas.from_strings(samples.title_akas_strings)
        self.assertEqual(obj.title_id, 'tt0000084')
        self.assertEqual(obj.ordering, 1)
        self.assertEqual(obj.title, 'The Drunkards')
        self.assertEqual(obj.region, 'GB')
        self.assertEqual(obj.language, None)
        self.assertEqual(obj.types, ['imdbDisplay'])
        self.assertEqual(obj.attributes, None)
        self.assertEqual(obj.is_original_title, False)


class TitleBasicsTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.title_basics.as_dict()
        expected = {
            'tconst': 'tt0000831',
            'title_type': 'short',
            'primary_title': 'The Cord of Life',
            'original_title': 'The Cord of Life',
            'is_adult': False,
            'start_year': 1909,
            'end_year': None,
            'runtime_minutes': 9,
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.TitleBasics.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitleBasics)

        # Many less than NUM_SAMPLE_ROWS as adult titles skipped by default
        self.assertEqual(count, 19_906)

        # Last record
        expected = readers.TitleBasics(
            tconst='tt9916880',
            title_type='tvEpisode',
            primary_title='Horrid Henry Knows It All',
            original_title='Horrid Henry Knows It All',
            is_adult=False,
            start_year=2014,
            end_year=None,
            runtime_minutes=10,
            genres=['Adventure', 'Animation', 'Comedy'],
        )
        self.assertEqual(expected, obj)

    def test_from_folder_no_skip_adult(self) -> None:
        reader = readers.TitleBasics.from_folder(DATA_FOLDER, skip_adult=False)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitleBasics)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

    def test_from_strings(self) -> None:
        obj = readers.TitleBasics.from_strings(samples.title_basics_strings)
        self.assertEqual(obj.tconst, 'tt0000831')
        self.assertEqual(obj.title_type, 'short')
        self.assertEqual(obj.primary_title, 'The Cord of Life')
        self.assertEqual(obj.original_title, 'The Cord of Life')
        self.assertEqual(obj.is_adult, False)
        self.assertEqual(obj.start_year, 1909)
        self.assertEqual(obj.end_year, None)
        self.assertEqual(obj.runtime_minutes, 9)
        self.assertEqual(obj.genres, ['Crime', 'Drama', 'Short'])


class TitleCrewTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.title_crew.as_dict()
        expected = {
            'tconst': 'tt0001004',
            'directors': ['nm0674600'],
            'writers': ['nm0275421,nm0304098'],
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.TitleCrew.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitleCrew)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

        # Last record
        expected = readers.TitleCrew(
            tconst='tt9916880',
            directors=['nm0584014', 'nm0996406'],
            writers=['nm1482639', 'nm2586970']
        )
        self.assertEqual(expected, obj)

    def test_from_strings(self) -> None:
        obj = readers.TitleCrew.from_strings(samples.title_crew_strings)
        self.assertEqual(obj.tconst, 'tt0001004')
        self.assertEqual(obj.directors, ['nm0674600'])
        self.assertEqual(obj.writers, ['nm0275421', 'nm0304098'])


class TitleEpisodesTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.title_episodes.as_dict()
        expected = {
            'tconst': 'tt0078459',
            'parent': 'tt0159876',
            'season': 6,
            'episode': 5,
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.TitleEpisodes.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitleEpisodes)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

        # Last record
        expected = readers.TitleEpisodes(
            tconst='tt9916880',
            parent='tt0985991',
            season=4,
            episode=2,
        )
        self.assertEqual(expected, obj)

    def test_from_strings(self) -> None:
        fields = ['tt0078459', 'tt0159876', '6', '5']
        obj = readers.TitleEpisodes.from_strings(fields)
        self.assertEqual(obj.tconst, 'tt0078459')
        self.assertEqual(obj.parent, 'tt0159876')
        self.assertEqual(obj.season, 6)
        self.assertEqual(obj.episode, 5)

    def test_from_strings_optional(self) -> None:
        fields = ['tt0078922', 'tt1686687', '\\N', '\\N']
        obj = readers.TitleEpisodes.from_strings(fields)
        self.assertEqual(obj.tconst, 'tt0078922')
        self.assertEqual(obj.parent, 'tt1686687')
        self.assertEqual(obj.season, None)
        self.assertEqual(obj.episode, None)


class TitlePrincipalsTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.title_principals.as_dict()
        expected = {
            'tconst': 'tt0000109',
            'ordering': 4,
            'nconst': 'nm0005658',
            'category': 'cinematographer',
            'job': None,
            'characters': None,
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.TitlePrincipals.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitlePrincipals)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

        # Last record
        expected = readers.TitlePrincipals(
            tconst='tt9916880',
            ordering=22,
            nconst='nm1482639',
            category='producer',
            job='producer',
            characters=None,
        )
        self.assertEqual(expected, obj)

    def test_from_strings(self) -> None:
        obj = readers.TitlePrincipals.from_strings(
            samples.title_principals_strings)
        self.assertEqual(obj.tconst, 'tt0000546')
        self.assertEqual(obj.ordering, 1)
        self.assertEqual(obj.nconst, 'nm0106151')
        self.assertEqual(obj.category, 'actor')
        self.assertEqual(obj.job, None)
        self.assertEqual(obj.characters, '["The Rarebit Fiend"]')

    def test_from_strings_optional(self) -> None:
        obj = readers.TitlePrincipals.from_strings(
            samples.title_principals_strings2)
        self.assertEqual(obj.tconst, 'tt0000109')
        self.assertEqual(obj.ordering, 4)
        self.assertEqual(obj.nconst, 'nm0005658')
        self.assertEqual(obj.category, 'cinematographer')
        self.assertEqual(obj.job, None)
        self.assertEqual(obj.characters, None)


class TitleRatingsTest(TestCase):
    def test_as_dict(self) -> None:
        data = samples.title_ratings.as_dict()
        expected = {
            'tconst': 'tt0000001',
            'average_rating': 4.5,
            'num_votes': 466,
        }
        self.assertEqual(data, expected)

    def test_from_folder(self) -> None:
        # Read all rows in sample folder
        reader = readers.TitleRatings.from_folder(DATA_FOLDER)
        for count, obj in enumerate(reader, 1):
            self.assertIsInstance(obj, readers.TitleRatings)

        # Number of lines minus header row
        self.assertEqual(count, NUM_SAMPLE_ROWS - 1)

        # Last record
        expected = readers.TitleRatings(
            tconst='tt9916880',
            average_rating=8.5,
            num_votes=7,
        )
        self.assertEqual(expected, obj)

    def test_from_strings(self) -> None:
        obj = readers.TitleRatings.from_strings(samples.title_ratings_strings)
        self.assertEqual(obj.tconst, 'tt0000001')
        self.assertEqual(obj.average_rating, 4.5)
        self.assertEqual(obj.num_votes, 466)
