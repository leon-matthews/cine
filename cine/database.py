
import logging
from pathlib import Path
import sqlite3
from typing import Optional

from .tables import AKAs, Episodes, Names, Principals, Ratings, Titles


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

        Args:
            path:
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
        """
        Various optimisations.
        """
        self.connection.execute('PRAGMA cache_size = -16384;')          # 16MiB
        self.connection.execute('PRAGMA journal_mode = WAL;')
        self.connection.execute('PRAGMA synchronous = OFF;')
        self.connection.execute('PRAGMA temp_store = MEMORY;')
