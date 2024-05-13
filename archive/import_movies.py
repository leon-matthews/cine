#!/usr/bin/env python

import pprint

import codecs
import json
import os
import cPickle as pickle

import imdb

"""
Import movies into collection.

Follows these steps:

Find title
1)  Identify possible movie file/folder
2)  Clean up name
3)  Search for name in IMDB
4)  If no obvious match found, prompt user with possible choices
5)  IMDB title found!

Move file/folder
6)  Create folder from title
7)  Move file or folder into collection, rename from title

Update metadata

8)  Fetch metadata.xml
    Use movie_id from step 3
        i = imdb.IMDb()
        movie = i.get_movie(movieID)

9)  Fetch folder.jpg
10) Generate about.mpg movie file
"""

ENCODING = 'utf-8'


class Importer(object):
    def __init__(self):
        self.imdb = imdb.IMDb()
        self.lookup_cache_path = 'cache.json'
        self.lookup_cache = {}
        self.choice_cache_path = 'choice.json'
        self.choice_cache = {}
        self.load_caches()

    def clean_name(self, name):
        """
        Clean given folder or file name.

        Best-effort tidy-up of file or folder name before passing it on to
        the lookup layer.
        """
        clean = name.strip()
        return clean

    def imdb_lookup(self, name):
        """
        Fetch title guesses from IMDB for the given name.

        Returns a list of movies matches, preserving the IMDB order.  Each
        match is a dictionary containing the keys: 'id', 'title', and 'year'.
        """
        results = self.imdb.search_movie(name)
        matches = []
        for movie in results:
            try:
                match = {}
                match['id'] = movie.movieID
                match['title'] = movie['long imdb title']
                match['year'] = movie['year']
                matches.append(match)
            except KeyError:
                pass
        return matches

    def choose_match(name, matches):
        """
        Chose the best matching IMDB title.

        name
            The source file/folder name
        matches
            An ordered list of match dictionaries
        """
        return matches[0]['title']


    def name_lookup(self, name):

        # Return if in cache
        if name in self.lookup_cache:
            return self.lookup_cache[name]

        matches = self.imdb_lookup(name)

        # Logging
        print u"Looking up '{0}' =>".format(name)
        if matches:
            print u"    {0} matches found, first: '{1}'".format(
                len(matches), matches[0]['title'] )
        else:
            print u"    No matches found!"

        # Add to cache
        if matches:
            self.lookup_cache[name] = matches

        return matches

    def save_caches(self):
        # Backup old cache files
        if os.path.isfile(self.lookup_cache_path):
            os.rename(self.lookup_cache_path, self.lookup_cache_path + '.bak')
        if os.path.isfile(self.choice_cache_path):
            os.rename(self.choice_cache_path, self.choice_cache_path + '.bak')

        # Create new cache files
        with codecs.open(self.lookup_cache_path, 'wt', encoding=ENCODING) as fp:
            json.dump(self.lookup_cache, fp, sort_keys=True, indent=4)
        with codecs.open(self.choice_cache_path, 'wt', encoding=ENCODING) as fp:
            json.dump(self.choice_cache, fp, sort_keys=True, indent=4)

    def load_caches(self):
        if os.path.isfile(self.lookup_cache_path):
            with codecs.open(
                self.lookup_cache_path, 'rt', encoding=ENCODING) as fp:
                self.lookup_cache = json.load(fp)
        if os.path.isfile(self.choice_cache_path):
            with codecs.open(
                self.choice_cache_path, 'rt', encoding=ENCODING) as fp:
                self.choice_cache = json.load(fp)


if __name__ == '__main__':
    # Open list of file/folder names
    names = []
    for name in codecs.open('movie_titles.txt', 'rt', encoding=ENCODING):
        names.append(name)

    # Search for names
    i = Importer()
    for name in names:
        try:
            name = i.clean_name(name)
            movie = i.name_lookup(name.strip())
        except:
            i.save_caches()
            raise
    i.save_caches()

