"""
Local SQLite3 database containing a sub-set of IMDB data.
"""


import itertools
import logging
import os
import textwrap
import time
import sqlite3


log = logging.getLogger(__name__)


class CreationResult:
    """
    Custom return type for database table creation methods.
    """

    format_spec = "{:<33} {:>9} {:>9} {:>9}"

    def __init__(self, name=None):
        """
        Initialiser

        name
            Name to use, usually set to name of file being imported.
        """
        self.name = name
        self.records = 0
        self.orphans = 0
        self.start = None
        self.end = None

    def timer_end(self):
        self.end = time.time()
        log.info("{:,} records inserted with {:,} orphans in {:.3f} seconds".format(
            self.records, self.orphans, self.end - self.start))

    def timer_start(self):
        self.start = time.time()

    def print_header(self):
        print(self.format_spec.format(
            'File', 'Records', 'Orphans', 'Seconds'))
        print(self.format_spec.format(
            '----', '-------', '-------', '-------'))

    def __str__(self):
        elapsed = ''
        if self.start and self.end:
            elapsed = '{:>8.1f}s'.format(self.end - self.start)
        return self.format_spec.format(
            self.name,
            '{:,}'.format(self.records),
            '{:,}'.format(self.orphans),
            elapsed)


class DB:
    """
    Database file wrapper.

    Database creation should be done in bulk, table by table, starting with
    the movies table.  It is assumed that tables are populated from monolithic
    IMDB flat files.
    """
    def __init__(self, path=None):
        """
        Initialise database.

        file
            Path to SQLite 3 database file.  Use None to create in-memory db.
        """
        if path is None:
            path = ':memory:'
        log.info("Create database: {}".format(os.path.abspath(path)))
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row   # Allow row access by name
        self.connection.execute('PRAGMA foreign_keys = ON;')
        self.connection.execute('PRAGMA synchronous = OFF;')
        self.connection.execute('PRAGMA journal_mode=MEMORY;')
        self.connection.execute('PRAGMA temp_store=MEMORY;')

    def find_movies(self, title):
        """
elect title, year from titles, movies where titles.title match 'die hard' and titles.docid==movies.docid;

SELECT name
FROM (
      SELECT name, 1 as matched
      FROM nametable
      WHERE name MATCH 'fast'
    UNION ALL
      SELECT name, 1 as matched
      FROM nametable
      WHERE name MATCH 'food'
    UNION ALL
      SELECT name, 1 as matched
      FROM nametable
      WHERE name MATCH 'restaurant'
  )
GROUP BY name
ORDER BY SUM(matched) DESC, name
        """
        raise NotImplementedError

    def get_genres(self):
        """
        SELECT genre, count(genre) AS genre_count FROM genres GROUP BY genre;
        """

    def create_actors(self, actors, actresses):
        """
        Populate actors table.
        """

        # Result object
        name = "{}, {}".format(actors.file_name, actresses.file_name)
        result = CreationResult(name)
        result.timer_start()

        # Delete existing data, if any
        self._drop_table('actors')
        self._drop_table('roles')

        # Create tables
        log.debug("Create tables: actors and roles")
        with self.connection as connection:
            connection.executescript(textwrap.dedent("""
                CREATE TABLE actors
                (
                    id          INTEGER PRIMARY KEY,
                    name        TEXT
                );

                CREATE TABLE roles
                (
                    id          INTEGER PRIMARY KEY,
                    character   TEXT,
                    actor_id    INTEGER REFERENCES actors(id),
                    movie_id    INTEGER REFERENCES movies(id)
                );
            """))

            # Insert data
            log.debug("Insert records into actors and roles")
            cursor = connection.cursor()
            for actor in itertools.chain(actors, actresses):
                cursor.execute(
                    "INSERT INTO actors VALUES(NULL,?);",
                    (actor.name,))
                actor_id = cursor.lastrowid
                for role in actor.roles:
                    cursor.execute(
                        "INSERT INTO roles "
                        "VALUES(NULL,?,?,"
                        "(SELECT id FROM movies WHERE title=?));",
                        (role.character, actor_id, role.title))

        # Fill in results object
        log.debug("Query database for record and orphan counts")
        with self.connection as connection:
            result.records = connection.execute(
                'SELECT count(*) FROM actors;').fetchone()[0]
            result.records += connection.execute(
                'SELECT count(*) FROM roles;').fetchone()[0]
            result.orphans = connection.execute(
                'SELECT count(*) FROM roles WHERE movie_id is NULL;'
                ).fetchone()[0]
        result.timer_end()
        return result

    def create_directors(self, directors):
        """
        Create and populate directors and director_credits tables.

        Returns two-tuple containing number total number of records inserted,
        and the number of orphaned records -- those with a bad reference back
        to the movies table.
        """

        # Result
        result = CreationResult(directors.file_name)
        result.timer_start()

         # Delete existing data, if any
        self._drop_table('directors')
        self._drop_table('director_credits')

        # Create tables
        log.debug("Create tables: directors and director_credits")
        with self.connection as connection:
            connection.executescript(textwrap.dedent("""
                CREATE TABLE directors
                (
                    id          INTEGER PRIMARY KEY,
                    name        TEXT
                );

                CREATE TABLE director_credits
                (
                    id          INTEGER PRIMARY KEY,
                    director_id INTEGER REFERENCES directors(id),
                    movie_id    INTEGER REFERENCES movies(id)
                );
            """))

            # Insert data
            log.debug("Insert records into directors and director_credits")
            cursor = connection.cursor()
            for director in directors:
                cursor.execute(
                    "INSERT INTO directors VALUES(NULL,?);", (director.name,))
                director_id = cursor.lastrowid
                for title in director.titles:
                    cursor.execute(
                        "INSERT INTO director_credits "
                        "VALUES(NULL,?,"
                        "(SELECT id FROM movies WHERE title=?));",
                        (director_id, title))

        # Calculate and return stats
        log.debug("Query database for record and orphan counts")
        with self.connection as connection:
            result.records += connection.execute(
                'SELECT count(*) FROM directors;'
                ).fetchone()[0]
            result.records += connection.execute(
                'SELECT count(*) FROM director_credits;'
                ).fetchone()[0]
            result.orphans = connection.execute(
                'SELECT count(*) FROM director_credits WHERE movie_id is NULL;'
                ).fetchone()[0]
        result.timer_end()
        return result

    def create_genres(self, genres):
        """
        Create and populate genres table.

        Returns two-tuple containing number total number of records inserted,
        and the number of orphaned records -- those with a bad reference back
        to the movies table.
        """
        # Result
        result = CreationResult(genres.file_name)
        result.timer_start()

        # Delete existing data
        self._drop_table('genres')

        # Insert data
        log.debug("Create table: genres")
        with self.connection as connection:
            connection.executescript(textwrap.dedent("""
                CREATE TABLE genres
                (
                    id          INTEGER PRIMARY KEY,
                    movie_id    INTEGER REFERENCES movies(id),
                    genre       TEXT
                );
            """))
            log.debug("Insert records into genres")
            connection.executemany(
                "INSERT INTO genres VALUES("
                "NULL,(SELECT id FROM movies WHERE title=?),?)", genres)

        # Calculate and return stats
        log.debug("Query database for record and orphan counts")
        with self.connection as connection:
            result.records = connection.execute(
                'SELECT count(*) FROM genres;'
                ).fetchone()[0]
            result.orphans = connection.execute(
                'SELECT count(*) FROM genres WHERE movie_id is NULL;'
                ).fetchone()[0]
        result.timer_end()
        return result

    def create_movies(self, movies):
        """
        Create movie tables table and populate with movies from iteratable.

        If table already exists it will be dropped -- although if any other
        tables have references to any of its records trying to do so will
        fail with a foreign key reference error.

        The movies table must be created before any other tables, given its
        central role in the database.

        Returns number of records inserted.
        """
        # Result
        result = CreationResult(movies.file_name)
        result.timer_start()

        # Delete exisiting data, if any
        self._drop_table('movies')

        # Create tables
        log.debug("Create table: movies")
        with self.connection as connection:
            connection.executescript(textwrap.dedent("""
                CREATE TABLE movies
                (
                    id          INTEGER PRIMARY KEY,
                    title       TEXT UNIQUE NOT NULL,
                    year        INTEGER
                );
            """))

            # Insert data
            log.debug("Insert records into movies")
            connection.executemany(
                "INSERT INTO movies VALUES(NULL,?,?)", movies)

        # Results
        log.debug("Query database for record counts")
        with self.connection as connection:
            result.records = connection.execute(
                'SELECT count(*) FROM movies;').fetchone()[0]
        result.timer_end()
        return result


    def create_ratings(self, ratings):
        """
        Create and populate ratings table.

        Existing ratings table will be dropped and recreated.

        Returns two-tuple containing number total number of records inserted,
        and the number of orphaned records -- those with a bad reference back
        to the movies table.
        """
        # Result
        result = CreationResult(ratings.file_name)
        result.timer_start()

        # Delete existing data
        self._drop_table('ratings')

        # Insert data
        log.debug("Create table: ratings")
        with self.connection as connection:
            connection.executescript(textwrap.dedent("""
                CREATE TABLE ratings
                (
                    id          INTEGER PRIMARY KEY,
                    movie_id    INTEGER REFERENCES movies(id),
                    rating      REAL NOT NULL,
                    votes       INTEGER NOT NULL
                );
            """))
            log.debug("Insert records into ratings")
            connection.executemany(
                "INSERT INTO ratings VALUES("
                "NULL,(SELECT id FROM movies WHERE title=?),?,?)", ratings)

        # Results
        log.debug("Query database for record and orphan counts")
        with self.connection as connection:
            result.records = connection.execute(
                'SELECT count(*) FROM ratings;'
                ).fetchone()[0]
            result.orphans = connection.execute(
                'SELECT count(*) FROM ratings WHERE movie_id is NULL;'
                ).fetchone()[0]
        result.timer_end()
        return result

    def _drop_table(self, table_name):
        """
        Drop table with given name.

        A no-op if the table doesn't actually exist.

        """
        try:
            log.debug("Drop table: {}".format(table_name))
            self.connection.execute("DROP TABLE ?;", table_name);
        except sqlite3.OperationalError:
            pass


class SearchDB:
    """
    Database for full text search of movie titles.

    Reads movie titles from existing database and creates separate search
    database from that.  Deleting the search database to save space is a safe
    operation as it can be re-generated at will.

    path_in
        Path to existing database containing raw data

    path_out
        Create output database at this path
    """
    def __init__(self, path_in, path_out):
        log.debug('Connect to database: %s', path_in)
        self.db_in = sqlite3.connect(path_in)
        log.debug('Connect to database: %s', path_out)
        self.db_out = sqlite3.connect(path_out)
        self.db_out.execute('PRAGMA synchronous = OFF;')
        self.db_out.execute('PRAGMA journal_mode=MEMORY;')
        self.db_out.execute('PRAGMA temp_store=MEMORY;')

    def create(self):
        log.info('Creating search database')
        with self.db_out:
            self.db_out.executescript(textwrap.dedent("""
                CREATE VIRTUAL TABLE movies_search USING fts4
                (
                    title       TEXT,
                    movie_id    INTEGER,
                    tokenize=porter
                );

                CREATE VIRTUAL TABLE actors_search USING fts4
                (
                    name        TEXT,
                    actor_id    INTEGER
                );

                CREATE VIRTUAL TABLE roles_search USING fts4
                (
                    name        TEXT,
                    role_id     INTEGER
                );
            """))

            log.info('Indexing movies...')
            self.db_out.executemany(
                "INSERT INTO movies_search VALUES(?,?);",
                self.db_in.execute('SELECT title, id FROM movies;'))

            log.info('Indexing actors...')
            self.db_out.executemany(
                "INSERT INTO actors_search VALUES(?,?);",
                self.db_in.execute('SELECT name, id FROM actors;'))

            log.info('Indexing roles...')
            self.db_out.executemany(
                "INSERT INTO roles_search VALUES(?,?);",
                self.db_in.execute('SELECT character, id FROM roles;'))
