
============
Introduction
============

Cine creates an SQLite database from IMDb Non-Commercial data files.


Dataset Details
===============

The data is provided by IMDb as 7 gzipped TSV files. The size grows constantly
as new movies and shows are released, but it's currently around 2GB compressed,
and 9GB as plain text.


People
------

Datasets involving people are keyed by what IMDb calls an `nconst`, for example
Fred Astaire's is `nm0000001`.

1. name.basics.tsv.gz - Peoples's basic biographical information, keyed
   by `nconst`, eg. `nm00000011`
2. title.crew.tsv.gz - Just the directors and writers of the title.
3. title.principals.tsv.gz - Rest of the cast and crew.

Titles
------

Datasets for movies and tv shows and any other type of work are keyed by a
`tconst`. For example Die Hard (1988) is uniquely identified by `tt0095016`.

1. title.basics.tsv.gz - Title name, release year, duration, genres
2. title.akas.tsv.gz  - Alternate names for titles over time or regions.
3. title.episode.tsv.gz - Season and episode numbers for TV.
4. title.ratings.tsv.gz - Ratings for titles and number of votes.


Database Design
===============

There are two approaches to building a database from the datasets.

1. An exhaustive approach where you preserve the structure and every single
   record in the source data (it might be useful one day!).

2. An opinionated approach, where you restructure freely and keep only the most
   useful records.


Opinionated
-----------

1. Read records in `title.ratings`. There are only about 1.5 million
   titles there, verses the 11 million titles in `title.basics`.
2. Write only those records from `title.basics` that also exist
   in `title.ratings`. Skip the pornos too.
