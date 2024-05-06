
import argparse
import csv
import gzip
from itertools import chain, islice
from pathlib import Path
from typing import Any, Iterable, Iterator


__all__ =  (
    'argparse_existing_folder',
    'chunkify',
    'to_bool',
    'to_bool_optional',
    'to_int_optional',
    'to_list',
    'to_list_optional',
    'to_str_optional',
    'tsv_imdb',
    'tsv_rows',
)


def argparse_existing_folder(string: str) -> Path:
    """
    Function for argparse 'type' keyword argument.

    Raises:
        argparse.ArgumentTypeError:
            If path does not exist.

    Returns:
        Path instance
    """
    path = Path(string).expanduser().resolve()

    error = None
    if not path.exists():
        error = f"Folder does not exist: {path}"
    elif not path.is_dir():
        error = f"Path is not a folder: {path}"

    if error is not None:
        raise argparse.ArgumentTypeError(error)

    return path


def chunkify(iterable: Iterable[Any], size: int) -> Iterator[Any]:
    """
    Generates sub-generators of `size` from given iterable.
    """
    iterator = iter(iterable)
    for first in iterator:
        yield chain((first,), islice(iterator, size - 1))


def to_bool(value: str) -> bool:
    return bool(int(value))


def to_bool_optional(value: str) -> bool|None:
    return None if value == r'\N' else bool(int(value))


def to_int_optional(value: str) -> int|None:
    return None if value == r'\N' else int(value)


def to_list(value: str) -> list[str]:
    return value.split(',')


def to_list_optional(value: str) -> list[str]|None:
    return None if value == r'\N' else value.split(',')


def to_str_optional(value: str) -> str|None:
    return None if value == r'\N' else value


class tsv_imdb(csv.excel_tab):
    """
    CSV dialect for tab-delimited IMDB data.
    """
    quoting = csv.QUOTE_NONE


def tsv_rows(path: Path, *,  skip_header: bool = False) -> Iterator[list[str]]:
    """
    Read compressed row data from IMDB TSV files, as distributed.

    Args:
        path:
            Path to gzipped TSV file.
        skip_header:
            Set to true to skip the first row of data.

    Returns:
        Generator over row data.
    """
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as fp:
        reader = csv.reader(fp, dialect=tsv_imdb)
        if skip_header:
            next(reader)
        yield from reader
