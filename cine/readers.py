"""
Extract and transform data from IMDB's compressed TSV data files.

The IMDB datasets are free for non-commercial use and are distributed as seven
gzip-compressed TSV files. As of 2024 these total 178 million data records.

The dataclasses below represent each type of data records and are able to
create themselves from the raw TSV files. Current documentation on fields can
be fould below, on the IMDb download page.

See:
    https://developer.imdb.com/non-commercial-datasets/
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, ClassVar, Iterator, Optional, Self

from .utils import (
    to_bool,
    to_bool_optional,
    to_int_optional,
    to_list,
    to_list_optional,
    to_str_optional,
    tsv_rows,
)


class Record:
    file_name: ClassVar[str]

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
        raise NotImplementedError('Sub-classes require from_strings() method')

    @classmethod
    def from_folder(cls, folder: Path) -> Iterator[Self]:
        """
        Build a record dataclasses from a gzipped TSV file.

        Args:
            folder:
                Folder containing downloaded IMDb *.tsv.gz files.

        Returns:
            Yields a single record instance per row in correct file.
        """
        path = folder / cls.file_name
        for row in tsv_rows(path, skip_header=True):
            yield cls.from_strings(row)


@dataclass
class NameBasics(Record):
    """
    Basic biographical details indexed by IMDb name indexes.
    """
    nconst: str                         # 'nm0000001'
    primary_name: str                   # 'Fred Astaire'
    birth_year: Optional[int]           # 1899
    death_year: Optional[int]           # 1987
    primary_profession: list[str]       # ['actor', 'miscellaneous', 'producer']
    known_for_titles: list[str]         # ['tt0072308', 'tt0050419',...]

    file_name: ClassVar[str] = 'name.basics.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        """
        Prepare data for database insertion.
        """
        data = asdict(self)
        del data['known_for_titles']
        del data['primary_profession']
        return data

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
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


@dataclass
class TitleAkas(Record):
    """
    Alternate title information.

    Lots of repeated title_ids (66 for The Matrix exapmle used below), often
    of each region or language.
    """
    title_id: str                       # 'tt0133093'
    ordering: int                       # 47
    title: str                          # 'Матрица'
    region: Optional[str]               # 'RU'
    language: Optional[str]             # None
    types: list[str]                    # 'imdbDisplay'
    attributes: Optional[list[str]]     # None
    is_original_title: Optional[bool]   # False

    file_name: ClassVar[str] = 'title.akas.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        """
        Prepare data for database insertion.
        """
        data = asdict(self)
        del data['attributes']
        del data['types']
        return data

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
        return cls(
            fields[0],
            int(fields[1]),
            fields[2],
            to_str_optional(fields[3]),
            to_str_optional(fields[4]),
            to_list(fields[5]),
            to_list_optional(fields[6]),
            to_bool_optional(fields[7]),
        )


@dataclass
class TitleBasics(Record):
    """
    Contains basic information for titles.
    """
    tconst: str                         # 'tt0133093'
    title_type: str                     # 'movie'
    primary_title: str                  # 'The Matrix'
    original_title: str                 # 'The Matrix'
    is_adult: bool                      # False
    start_year: Optional[int]           # 1999
    end_year: Optional[int]             # None
    runtime_minutes: Optional[int]      # 136
    genres: list[str]                   # ['Action', 'Sci-Fi']

    file_name: ClassVar[str] = 'title.basics.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        fields = asdict(self)
        del fields['genres']
        return fields

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
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
    def from_folder(cls, folder: Path, skip_adult: bool = True) -> Iterator[Self]:
        """
        Skip pornographic titles by default.

        Args:
            skip_adult:
                Set to false to read XXX titles.

        Returns:
            Yields instances of itself.
        """
        for obj in super(cls, cls).from_folder(folder):
            if skip_adult and obj.is_adult:
                continue
            yield obj


@dataclass
class TitleCrew(Record):
    """
    Contains the director and writer information for all the titles in IMDb.
    """
    tconst: str                         # 'tt0133093'
    directors: list[str]                # ['nm0905154', 'nm0905152']
    writers: list[str]                  # ['nm0905152', 'nm0905154']

    file_name: ClassVar[str] = 'title.crew.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
        return cls(
            fields[0],
            to_list(fields[1]),
            to_list(fields[2]),
        )


@dataclass
class TitleEpisodes(Record):
    """
    Contains the TV episode information.

    Multiple records per TV show. For example, 'Star Trek: Voyager' has
    168 records, one per episode.
    """
    tconst: str                         # 'tt0795288'
    parent: str                         # 'tt0112178'
    season: Optional[int]               # 5
    episode: Optional[int]              # 17

    file_name: ClassVar[str] = 'title.episode.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
        return cls(
            fields[0],
            fields[1],
            to_int_optional(fields[2]),
            to_int_optional(fields[3]),
        )


@dataclass
class TitlePrincipals(Record):
    """
    Contains the principal cast/crew for titles
    """
    tconst: str                         # 'tt0112178'
    ordering: int                       # 1
    nconst: str                         # 'nm0000550'
    category: str                       # 'actress'
    job: Optional[str]                  # None
    characters: Optional[str]           # 'Capt. Kathryn Janeway'

    file_name: ClassVar[str] = 'title.principals.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
        return cls(
            fields[0],
            int(fields[1]),
            fields[2],
            fields[3],
            to_str_optional(fields[4]),
            to_str_optional(fields[5]),
        )


@dataclass
class TitleRatings(Record):
    """
    Contains the IMDb rating and votes information for titles
    """
    tconst: str                         # 'tt0795288'
    average_rating: float               # 7.5
    num_votes: int                      # 2150

    file_name: ClassVar[str] = 'title.ratings.tsv.gz'

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_strings(cls, fields: list[str]) -> Self:
        return cls(
            fields[0],
            float(fields[1]),
            int(fields[2]),
        )
