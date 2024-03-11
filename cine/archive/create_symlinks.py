#!/usr/bin/env python

"""
Version of by_year.py using custom XML parsing, for speed.
"""
import collections
import os
import logging
import pickle
import pprint

# Element tree API -- lxml is slightly faster, but not always available
try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree

import cine

from lxml import etree



# Setup logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

def build_movie_mapping(titles, generateKeys):
    # Custom key to movie list mapping
    movies = collections.defaultdict(list)
    for title in titles:
        # Build ElementTree object with metadata
        path = data._generate_xml_path(title)
        if not os.path.isfile(path):
            continue
        doc = etree.ElementTree(file=path)
        # Get custom mapping keys, eg. cast members
        keys = generateKeys(doc)
        # Build mapping
        for key in keys:
            movies[key].append(title)
    return movies

def findYear(doc):
    """
    Return iterable of keys whost lists movie title should be added to.
    """
    elem = doc.find('year')
    year = elem.text
    return (year,)

def findGenres(doc):
    """
    Return iterable of keys whost lists movie title should be added to.
    """
    genres = set()
    for elem in doc.findall('genres/item'):
        genres.add(elem.text)
    return genres

def findCast(doc):
    cast = set()
    for elem in doc.findall('cast/person/name'):
        cast.add(elem.text)
    return cast

def findWriters(doc):
    writers = set()
    for elem in doc.findall('writer/person/name'):
        writers.add(elem.text)
    return writers

def findDirectors(doc):
    directors = set()
    for elem in doc.findall('director/person/name'):
        directors.add(elem.text)
    return directors

def findRating(doc):
    elem = doc.find('rating')
    rating = float(elem.text)
    rating = '{0:.1f}'.format(rating)
    return (rating,)

def findCountries(doc):
    countries = set()
    for elem in doc.findall('countries/item'):
        countries.add(elem.text)
    return countries

def print_movie_mapping(movie_map, minimum=0):
    for key in sorted(movie_map):
        movies = movie_map[key]
        if len(movies) < minimum:
            continue
        print key
        pprint.pprint(movies, width=1)
        print

def create_symlinks(base_folder, movie_map, titles, minimum=0):
    for key in sorted(movie_map):

        # Check number of movies under mapping
        movies = movie_map[key]
        if len(movies) < minimum:
            continue

        folder = os.path.join(base_folder, key)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        print key
        print "="*len(key)
        for title in movies:
            path = titles[title]
            print "%s" % title
            print "  => %s" % titles[title]
            link_name = os.path.join(folder, os.path.basename(path))
            if not os.path.exists(link_name):
                print link_name
                os.symlink(path, link_name)
        print


if __name__ == '__main__':

    movie_folder = '/srv/movies/all/'
    c = cine.collection.Reader(movie_folder)

    metadata_folder = '/srv/movies/metadata/'
    data = cine.metadata.Metadata(metadata_folder)

    symlink_folder = '/srv/movies/symlinks'


    titles = c.titles

    # Cast
    folder = os.path.join(symlink_folder, 'by_cast')
    mapping = build_movie_mapping(titles, findCast)
    create_symlinks(folder, mapping, titles, 10)

    # Director
    folder = os.path.join(symlink_folder, 'by_director')
    mapping = build_movie_mapping(titles, findDirectors)
    create_symlinks(folder, mapping, titles, 3)

    # Genre
    folder = os.path.join(symlink_folder, 'by_genre')
    mapping = build_movie_mapping(titles, findGenres)
    create_symlinks(folder, mapping, titles)

    # Year
    folder = os.path.join(symlink_folder, 'by_year')
    mapping = build_movie_mapping(titles, findYear)
    create_symlinks(folder, mapping, titles)

    # Rating
    folder = os.path.join(symlink_folder, 'by_rating')
    mapping = build_movie_mapping(titles, findRating)
    create_symlinks(folder, mapping, titles)

    # Writer
    folder = os.path.join(symlink_folder, 'by_writer')
    mapping = build_movie_mapping(titles, findWriters)
    create_symlinks(folder, mapping, titles, 3)

