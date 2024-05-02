"""
Extract and transform data from IMDB's compressed TSV data files.

The IMDB datasets (see README.txt for download and documentation links) are
distributed as seven gzip-compressed TSV files. As of 2022 these total
122 million records.

The seven dataclass classes below represent each row of data. Each has a
``from_strings()`` method that converts the string data into Python data types
and a ``from_folder()`` method that builds a generator over every record from
its corresponding file.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from pprint import pprint as pp
from typing import Any, Callable, Iterator, Optional

from .utils import tsv_rows


def to_bool(value: str) -> bool:
    return bool(int(value))


def to_bool_optional(value: str) -> Optional[bool]:
    return None if value == r'\N' else bool(int(value))


def to_int_optional(value: str) -> Optional[int]:
    return None if value == r'\N' else int(value)


def to_list(value: str) -> list[str]:
    return value.split(',')


def to_list_optional(value: str) -> Optional[list[str]]:
    return None if value == r'\N' else value.split(',')


def to_str_optional(value: str) -> Optional[str]:
    return None if value == r'\N' else value


class Record:
    pass


@dataclass
class NameBasics(Record):
    """
    Contains basic information for names.
    """
    nconst: str
    primary_name: str
    birth_year: Optional[int]
    death_year: Optional[int]
    primary_profession: list[str]
    known_for_titles: list[str]

    def as_dict(self) -> dict[str, Any]:
        """
        Prepare data for database insertion.
        """
        data = asdict(self)
        del data['known_for_titles']
        del data['primary_profession']
        return data

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'NameBasics':
        """
        Build database from list of strings from TSV file.
        """
        return cls(
            fields[0],
            fields[1],
            to_int_optional(fields[2]),
            to_int_optional(fields[3]),
            to_list(fields[4]),
            to_list(fields[5]),
        )

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator['NameBasics']:
        """
        Build LOTS of dataclasses from a gzipped TSV file.
        """
        path = folder / 'name.basics.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)


@dataclass
class TitleAkas(Record):
    """
    Alternate title information.
    """
    title_id: str
    ordering: int
    title: str
    region: str
    language: Optional[str]
    types: list[str]
    attributes: Optional[list[str]]
    is_original_title: Optional[bool]

    def as_dict(self) -> dict[str, Any]:
        """
        Prepare data for database insertion.
        """
        data = asdict(self)
        del data['attributes']
        del data['types']
        return data

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'TitleAkas':
        return cls(
            fields[0],
            int(fields[1]),
            fields[2],
            fields[3],
            to_str_optional(fields[4]),
            to_list(fields[5]),
            to_list_optional(fields[6]),
            to_bool_optional(fields[7]),
        )

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator['TitleAkas']:
        path = folder / 'title.akas.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)


@dataclass
class TitleBasics(Record):
    """
    Contains basic information for titles.
    """
    tconst: str
    title_type: str
    primary_title: str
    original_title: str
    is_adult: bool
    start_year: Optional[int]
    end_year: Optional[int]
    runtime_minutes: Optional[int]
    genres: list[str]

    def as_dict(self) -> dict[str, Any]:
        fields = asdict(self)
        del fields['genres']
        return fields

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'TitleBasics':
        return cls(
            fields[0],
            fields[1],
            fields[2],
            fields[3],
            to_bool(fields[4]),
            to_int_optional(fields[5]),
            to_int_optional(fields[6]),
            to_int_optional(fields[7]),
            to_list(fields[8]),
        )

    @classmethod
    def from_folder(
        cls,
        folder: Path,
        *,
        skip_adult: bool = True
    ) -> Iterator['TitleBasics']:
        path = folder / 'title.basics.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            obj = cls.from_strings(row)
            if skip_adult and obj.is_adult:
                continue
            yield obj


@dataclass
class TitleCrew(Record):
    """
    Contains the director and writer information for all the titles in IMDb.
    """
    tconst: str
    directors: list[str]
    writers: list[str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'TitleCrew':
        return cls(
            fields[0],
            to_list(fields[1]),
            to_list(fields[2]),
        )

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator['TitleCrew']:
        path = folder / 'title.crew.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)


@dataclass
class TitleEpisodes(Record):
    """
    Contains the TV episode information.
    """
    tconst: str
    parent: str
    season: Optional[int]
    episode: Optional[int]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'TitleEpisodes':
        return cls(
            fields[0],
            fields[1],
            to_int_optional(fields[2]),
            to_int_optional(fields[3]),
        )

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator['TitleEpisodes']:
        path = folder / 'title.episode.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)


@dataclass
class TitlePrincipals(Record):
    """
    Contains the principal cast/crew for titles
    """
    tconst: str
    ordering: int
    nconst: str
    category: str
    job: Optional[str]
    characters: Optional[str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'TitlePrincipals':
        return cls(
            fields[0],
            int(fields[1]),
            fields[2],
            fields[3],
            to_str_optional(fields[4]),
            to_str_optional(fields[5]),
        )

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator['TitlePrincipals']:
        path = folder / 'title.principals.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)


@dataclass
class TitleRatings(Record):
    """
    Contains the IMDb rating and votes information for titles
    """
    tconst: str
    average_rating: float
    num_votes: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> 'TitleRatings':
        return cls(
            fields[0],
            float(fields[1]),
            int(fields[2]),
        )

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator['TitleRatings']:
        path = folder / 'title.ratings.tsv.gz'
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)
