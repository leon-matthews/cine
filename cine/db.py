
import logging
from pathlib import Path
from pprint import pprint as pp
import sqlite3
import textwrap
from time import perf_counter
from typing import Any, Iterable, Optional, Tuple

from . import readers, utils


logger = logging.getLogger(__name__)


class Database:
    """
    Local copy of IMDb title, cast, and rating data.

    Providely freely by IMDb, licensed for non-commercial and non-competing
    usage.

    See:
        https://developer.imdb.com/non-commercial-datasets/
    """
    def __init__(self, path: Optional[Path|str] = None):
        """
        Initialise database.

        file
            Path to SQLite 3 database file to use or create.
            Use the default of `None` to create in-memory db.

        """
        # Database file
        if path is None:
            path = ':memory:'
        logger.debug("Connect to database:  '%s'", path)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self._run_pragmas()

        # Database tables
        self.akas = AKAs(self)
        self.episodes = Episodes(self)
        self.titles = Titles(self)
        self.names = Names(self)
        self.principals = Principals(self)
        self.ratings = Ratings(self)

    def backup(self, path: Path) -> None:
        logger.info("Back-up database to: %s", path)
        destination = sqlite3.connect(path)
        self.connection.backup(destination)

    def cursor(self) -> sqlite3.Cursor:
        return self.connection.cursor()

    def get_table_names(self) -> list[str]:
        """
        Fetch a list of table names.

        Returns:
            Sorted list of database table names.
        """
        query = 'SELECT name from sqlite_master where type= "table"'
        cursor = self.connection.execute(query)
        names = [row[0] for row in cursor.fetchall()]
        return sorted(names)

    def _run_pragmas(self) -> None:
        self.connection.execute('PRAGMA cache_size = -16384;')    # 16MiB
        self.connection.execute('PRAGMA journal_mode = WAL;')
        self.connection.execute('PRAGMA synchronous = OFF;')
        self.connection.execute('PRAGMA temp_store = MEMORY;')


class TableBase:
    """
    Common functionality for database tables.

    Attributes:
        insert_query:
            SQL statement to insert a new row of data.
        records_per_transaction:
            When inserting many records, wrap this many records in a single
            transaction as an optimisation.
        table_name:
            String containing table name.
        table_query:
            SQL statement to create database table.

    """
    insert_query: str
    records_per_transaction: int = 10_000
    table_name: str
    table_query: str

    def __init__(self, db: Database):
        """
        Args:
            db:
                Reference to the `Database` instance to which table belongs.
        """
        self.db = db
        self.create_table()

    def count(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.table_name};"
        cursor = self.db.connection.execute(query)
        count = cursor.fetchone()[0]
        assert isinstance(count, int)
        return count

    def create_table(self) -> None:
        """
        Create database table only if requuired.
        """
        query = textwrap.dedent(self.table_query).strip()
        self.db.connection.execute(query)

    def insert(self, record: readers.Record) -> int:
        """
        Insert a single record.

        Returns:
            The id of the row inserted.
        """
        fields = record.as_dict()
        cursor = self.db.connection.execute(self.insert_query, fields)
        pk = cursor.lastrowid
        assert isinstance(pk, int)
        return pk

    def insert_many(self, records: Iterable[readers.Record]) -> None:
        start = perf_counter()
        num_added = 0
        cursor = self.db.cursor()
        for chunk in utils.chunkify(records, self.records_per_transaction):
            chunk_start = perf_counter()
            cursor.execute('BEGIN;')
            cursor.executemany(self.insert_query, records)
            cursor.execute('COMMIT;')
            num_added += len(chunk)
            elapsed = perf_counter() - chunk_start
            logger.debug(
                f"Added {len(chunk):,} records to database in "
                f"{elapsed:.3f} seconds ({num_added:,} total)"
            )

        total_time = perf_counter() - start
        logger.info(f"{num_added:,} records in {total_time:.3f} seconds")

    def select(self, pk: int) -> dict[str, Any]:
        query = f"SELECT * FROM {self.table_name} WHERE rowid=?;"
        cursor = self.db.connection.execute(query, (pk,))
        row = cursor.fetchone()
        return dict(row)


class AKAs(TableBase):
    """

    """
    insert_query = (
        "INSERT INTO akas VALUES (:title_id, :ordering, :title, :region, "
        ":language, :is_original_title);"
    )
    table_name = 'akas'
    table_query = """
        CREATE TABLE IF NOT EXISTS akas (
            title_id            TEXT,
            ordering            INTEGER,
            title               TEXT,
            region              TEXT,
            language            TEXT,
            is_original_title   BOOL
            -- attributes
            -- types
        );
    """


class Episodes(TableBase):
    """
    TV episode data from 'title.episode.tsv'.

    Every TV episode has an entry in the titles table, pointed to by the
    ``tconst``, and another for the whole show itself in ``parent``.

    """
    insert_query = (
        "INSERT INTO episodes VALUES (:tconst, :parent, :season, :episode);"
    )
    table_name = 'episodes'
    table_query = """
        CREATE TABLE IF NOT EXISTS episodes (
            tconst              TEXT,
            parent              TEXT,
            season              INTEGER,
            episode             INTEGER
        );
    """


class Names(TableBase):
    """
    Database table containing people's basic data found in 'name.basics.tsv'.

    TODO:
        - Convert nconst into an integer, eg 'nm00000435' => 435
        - Declare nconst is primary key, then table 'WITHOUT ROWID'

    """
    insert_query = (
        "INSERT INTO names VALUES (:nconst, :primary_name, :birth_year, :death_year);"
    )
    table_name = 'names'
    table_query = """
        CREATE TABLE IF NOT EXISTS names (
            nconst              TEXT,
            primary_name        TEXT,
            birth_year          INTEGER,
            death_year          INTEGER
            -- primary_profession?
            -- known_for_titles?
        );
        """


class Principals(TableBase):
    """
    Contains the principal cast/crew for titles.
    """
    insert_query = (
        "INSERT INTO principals VALUES ("
        ":tconst, :ordering, :nconst, :category, :job, :characters);"
    )
    table_name = "principals"
    table_query = """
        CREATE TABLE IF NOT EXISTS principals (
            tconst              TEXT,
            ordering            INTEGER,
            nconst              TEXT,
            category            TEXT,
            job                 TEXT,
            characters          TEXT
        );
    """


class Ratings(TableBase):
    """
    Contains the IMDb rating and votes information for titles.

    TODO:
        - Change 'average_rating' to an integer (ie. in tenths)

    """
    insert_query = (
        "INSERT INTO ratings VALUES (:tconst, :average_rating, :num_votes);"
    )
    table_name = 'ratings'
    table_query = """
        CREATE TABLE IF NOT EXISTS ratings (
            tconst              TEXT,
            average_rating      REAL,
            num_votes           INTEGER
        );
    """


class Titles(TableBase):
    """
    Table holding the titles movies and shows from 'titles.basics.tsv'.

    TODO:
        - Convert 'tconst' to an integer, eg. 'tt0000992' => 992
        - Make 'title_type' an integer key in fixed enums
        - Don't save 'original_title' if it's the same as 'primary_title'
        - Just skip 'is_adult' rows completely?
        - Declare tconst as primary key, then table 'WITHOUT ROWID'

    """
    insert_query = (
        "INSERT INTO titles values (:tconst, :title_type, :primary_title, "
        ":original_title, :is_adult, :start_year, :end_year, :runtime_minutes);"
    )
    table_name = 'titles'
    table_query = """
        CREATE TABLE IF NOT EXISTS titles (
            tconst              TEXT,
            title_type          TEXT,
            primary_title       TEXT,
            original_title      TEXT,
            is_adult            BOOL,
            start_year          INTEGER,
            end_year            INTEGER,
            runtime_minutes     INTEGER
            -- genres?
        );
        """
