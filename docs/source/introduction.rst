
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
