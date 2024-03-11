
from pathlib import Path
from string import ascii_lowercase
from unittest import TestCase

from cine.utils import chunkify, tsv_rows

from . import DATA_FOLDER


class ChunkifyTest(TestCase):
    def test_chunkify(self) -> None:
        letters = list(ascii_lowercase)
        self.assertEqual(len(letters), 26)
        chunks = []
        for chunk in chunkify(letters, 10):
            chunks.append(''.join(chunk))
        self.assertEqual(chunks, ['abcdefghij', 'klmnopqrst', 'uvwxyz'])


class TsvRowsTest(TestCase):
    path = DATA_FOLDER / 'title.ratings.tsv.gz'

    def test_read_rows(self) -> None:
        """
        There are 1,000 rows, each row is a list of strings.
        """
        reader = tsv_rows(self.path)
        for count, row in enumerate(reader, 1):
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), 3)
            for column in row:
                self.assertIsInstance(column, str)
        self.assertEqual(count, 1_000)

    def test_skip_header(self) -> None:
        reader = tsv_rows(self.path, skip_header=True)
        rows = list(reader)
        self.assertEqual(len(rows), 999)

    def test_not_found(self) -> None:
        path = Path('/no/such/file')
        reader = tsv_rows(path)
        message = r"^\[Errno 2\] No such file or directory: '/no/such/file'$"
        with self.assertRaisesRegex(FileNotFoundError, message):
            next(reader)
