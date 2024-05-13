"""
Populate local database from IMDB alternative access data files.
"""

import logging
import os
import sys
import time

from . import db
from . import readers


log = logging.getLogger(__name__)


class Importer:
    """
    Import IMDB alternative access data files into local database.

    Mediates between the reader and database classes.
    """

    def __init__(self, data_folder, database_file):
        """
        Initialise Importer object.

        data_folder
            Path to folder containing IMDb alternative access data files,
            still in gzip compressed formate.
        database_file
            Path to local SQLite3 database file to create.  Defaults to
            'imdb.db' in the current working folder.
        """
        log.info("Importing from: {}".format(os.path.abspath(data_folder)))
        self.folder = data_folder
        self.database_file = database_file
        self.database = db.DB(self.database_file)

    def import_actors(self):
        log.info("Import actors and their roles")
        actors = readers.ActorReader(self.folder)
        actresses = readers.ActressReader(self.folder)
        return self.database.create_actors(actors, actresses)

    def import_directors(self):
        log.info("Import directors")
        directors = readers.DirectorReader(self.folder)
        return self.database.create_directors(directors)

    def import_genres(self):
        log.info("Import genres")
        genres = readers.GenreReader(self.folder)
        return self.database.create_genres(genres)

    def import_movies(self):
        """
        Import movies table, resetting the whole database.

        The movies table is referenced by all other data tables.  Recreating
        it requires that all other tables be deleted too.  The fastest way
        to do this to to simply delete the database file.
        """
        log.info("Import movies")
        movies = readers.MovieReader(self.folder)
        return self.database.create_movies(movies)

    def import_ratings(self):
        log.info("Import ratings")
        ratings = readers.RatingReader(self.folder)
        return self.database.create_ratings(ratings)
