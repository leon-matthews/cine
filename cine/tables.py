
from __future__ import annotations

import abc
from dataclasses import asdict
import logging
import textwrap
import time
from typing import Any, Iterable

from . import database
from .readers import Record
from .utils import chunkify


logger = logging.getLogger(__name__)


class TableBase(abc.ABC):
    """
    Common functionality for an individual database table.

    For each new table, extend this class and fill-in the class attributes
    for the table name and SQL query templates.
    """
    # SQL statement to insert a new row of data.
    insert_query: str

    # Chunk size for insertion optimisation
    records_per_transaction: int = 10_000

    # String containing table name.
    table_name: str

    # SQL statement to create database table.
    table_query: str

    def __init__(self, db: database.Database):
        """
        Args:
            db:
                Reference to the `Database` instance to which table belongs.
        """
        self.db = db
        self.create_table()

    def __init_subclass__(child_class: type, **kwargs: Any) -> None:
        """
        Give a good error message if child classes are missing required
        class attributes.

        Raises:
            NotImplementedError:
                If child class missing required attributes.
        """
        required = ('insert_query', 'table_name', 'table_query')
        missing = []
        for name in required:
            if not hasattr(child_class, name):
                missing.append(name)

        if missing:
            attrs = ', '.join(missing)
            message = f"{child_class.__name__} missing required attributes: {attrs}"
            raise NotImplementedError(message)

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

    def insert(self, record: Record) -> int:
        """
        Insert a single record.

        Returns:
            The id of the row inserted.
        """
        fields = asdict(record)
        cursor = self.db.connection.execute(self.insert_query, fields)
        pk = cursor.lastrowid
        assert isinstance(pk, int)
        return pk

    def insert_many(self, records: Iterable[Record]) -> None:
        start = time.perf_counter()
        num_added = 0
        cursor = self.db.cursor()
        for chunk in chunkify(records, self.records_per_transaction):
            chunk_start = time.perf_counter()
            cursor.execute('BEGIN;')
            cursor.executemany(self.insert_query, records)
            cursor.execute('COMMIT;')
            num_added += len(chunk)
            elapsed = time.perf_counter() - chunk_start
            logger.debug(
                f"Added {len(chunk):,} records to database in "
                f"{elapsed:.3f} seconds ({num_added:,} total)"
            )

        total_time = time.perf_counter() - start
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
