
from argparse import ArgumentTypeError
from pathlib import Path
from string import ascii_lowercase
from unittest import TestCase

from cine.utils import *

from . import DATA_FOLDER, NUM_SAMPLE_ROWS


class ArgparseExistingFolderTest(TestCase):
    def test_folder_exists(self):
        string = str(Path(__file__).parent)
        folder = argparse_existing_folder(string)
        self.assertIsInstance(folder, Path)
        self.assertTrue(folder.is_dir())

    def test_is_file(self) -> None:
        message = r"^Path is not a folder: .*"
        with self.assertRaisesRegex(ArgumentTypeError, message):
            argparse_existing_folder(__file__)

    def test_is_nonsense(self) -> None:
        message = r"^Folder does not exist: .*"
        with self.assertRaisesRegex(ArgumentTypeError, message):
            argparse_existing_folder('banana')


class ChunkifyTest(TestCase):
    def test_chunkify(self) -> None:
        letters = list(ascii_lowercase)
        self.assertEqual(len(letters), 26)
        chunks = []
        for chunk in chunkify(letters, 10):
            chunks.append(''.join(chunk))
        self.assertEqual(chunks, ['abcdefghij', 'klmnopqrst', 'uvwxyz'])


class ConverterTest(TestCase):
    def test_to_list(self) -> None:
        self.assertEqual(to_list(r'\N'), [r'\N'])

    def test_to_list_optional(self) -> None:
        self.assertEqual(to_list_optional(r'\N'), [])


class TsvRowsTest(TestCase):
    path = DATA_FOLDER / 'title.ratings.tsv.gz'

    def test_read_rows(self) -> None:
        """
        There are many rows, each of which should be a list of strings.
        """
        reader = tsv_rows(self.path)
        for count, row in enumerate(reader, 1):
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), 3)
            for column in row:
                self.assertIsInstance(column, str)

        self.assertEqual(count, NUM_SAMPLE_ROWS)

    def test_skip_header(self) -> None:
        reader = tsv_rows(self.path, skip_header=True)
        rows = list(reader)
        self.assertEqual(len(rows), NUM_SAMPLE_ROWS - 1)

    def test_not_found(self) -> None:
        path = Path('/no/such/file')
        reader = tsv_rows(path)
        message = r"^\[Errno 2\] No such file or directory: '/no/such/file'$"
        with self.assertRaisesRegex(FileNotFoundError, message):
            next(reader)
