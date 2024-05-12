"""
Utility functions
"""

import re


def clean_title(title):
    """
    Clean and validate given title.

    title
        Should be in IMDB cannonical format.  A nicely formated file name
        will suffice, as any extension will be trimmed off.

    Raises ValueError if title doesn't match expected format.
    """
    title = title.strip()
    match = clean_title._CLEAN_TITLE_REGEX.search(title)
    if match is None:
        raise ValueError("Title format error: '{}'".format(title))
    title = match.group('title')
    return title


clean_title._CLEAN_TITLE_REGEX = re.compile(r'''
    ^                           # (start)
    (\d\d\.\s)?                 # Possible prefix, eg. '13. '
    (?P<title>                  # capture title
    \w                          # start of title must be alphanumeric
    [\w\s\d\.\-(),!'&]*         # title string
    \s                          # space
    \(\d{4}\)                   # 4-digit year in parentheses
    )                           # end title capture
    (\.\w+)?                    # Possible extension
    $                           # (end)
    ''', re.VERBOSE)


def extract_year(title):
    """Extract year from title.

    Returns year as integer, or None if unknown.
    """
    match = extract_year.regex.search(title)
    if match is None:
        return None
    return int(match.group(1))
extract_year.regex = re.compile(r'\((\d{4})')


def guess_type(title):
    """
    Return string giving type of title.

    The titles in the database fall into one of five categories:

        1. Movies, unless otherwise indicated the title is a movie
        2. Made for TV movies, indicated by a (TV) tag
        3. Made for video movies, indicated by a (V) tag
        4. TV-series, indicated by enclosing the title in "'s
        5. Mini-series, indicated by enclosing the title in "'s
           and a (mini) tag

    TODO
        Return smarter object than can be queried, eg. for tv
        episode number.
    """
    if title.startswith('"'):
        return 'tv-series'
    elif '(TV)' in title:
        return 'straight-to-tv'
    elif '(V)' in title:
        return 'straight-to-dvd'
    return 'movie'


def uncomma_name(name):
    """Un-comma a name, eg. 'Matthews, Leon' => 'Leon Matthews'
    """
    try:
        comma = name.rindex(',')
        return "{} {}".format(name[comma+2:], name[0:comma])
    except ValueError:
        return name
