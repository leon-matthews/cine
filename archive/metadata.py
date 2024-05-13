"""
Responsible for fetching movie metadata.
"""

import os
import sys
import urllib2

import imdb
import imdb.helpers


class Metadata(object):
    """
    Manages collection of metadata for movies, including images.

    Metadata is downloaded from imdb.com using the IMDbPY package, and is cached
    locally as XML and image files under the given folder.

    Three kinds of objects are used in the API: Titles, paths, and movies.

    Titles
        Unicode strings in the IMDB cannonical form, eg. 'The Prestige (2006)'
    Paths
        Strings containing file-system paths.
    Movies
        The heavy lifting is performed by IMDbPY.  Instances of its imdb.Movie
        class hold all of the movie metadata.
    """
    def __init__(self, folder):
        self.imdb_access = imdb.IMDb()
        # Define/create folders
        assert os.path.isdir(folder), (
            "Metadata folder not found: '{0}'".format(folder))
        self.POSTER_FOLDER = os.path.join(folder, 'posters')
        self.XML_FOLDER = os.path.join(folder, 'xml')
        if not os.path.isdir(self.POSTER_FOLDER):
            os.mkdir(self.POSTER_FOLDER)
        if not os.path.isdir(self.XML_FOLDER):
            os.mkdir(self.XML_FOLDER)

    def get_movie(self, title):
        """
        Return movie object with given title, from cache or Internet.
        """
        # Load from pickle file
        path = self._generate_xml_path(title)
        try:
            movie = self._load_xml(path)
        except IOError:
            # Fetch from Internet
            movie = self._fetch_movie(title)
        return movie

    def get_poster(self, title):
        """
        Return path to poster image, from cache or Internet.
        """
        path = self._generate_poster_path(title)
        if os.path.isfile(path):
            return path
        # Fetch from Internet
        path = self._fetch_poster(title)
        return path

    def flush(self, title):
        """
        Delete cache entries for given title.
        """
        path = self._generate_xml_path(title)
        if os.path.isfile(path):
            os.remove(path)
        path = self._generate_poster_path(title)
        if os.path.isfile(path):
            os.remove(path)

    def titles_excess(self, titles):
        """
        Calculate set of titles with cache entries excess to given title list.
        titles
            Iterable of titles, eg. ['Dinosaur (2000)', 'Pi (1998)',]
        Returns set of title strings.
        """
        poster_cache = self._cached_posters()
        xml_cache = self._cached_xml()
        excess = (set(xml_cache) | set(poster_cache)) - set(titles)
        return excess

    def titles_missing(self, titles):
        """
        Calculate set of titles from given title list not found in cache.
        titles
            Iterable of titles, eg. ['Dinosaur (2000)', 'Pi (1998)',]
        Returns set of title strings
        """
        poster_cache = self._cached_posters()
        xml_cache = self._cached_xml()
        missing = set(titles) - set(poster_cache)
        missing |= set(titles) - set(xml_cache)
        return missing

    def _cached_posters(self):
        """
        Return list of titles for which we have cached poster images for.
        """
        files = os.listdir(self.POSTER_FOLDER)
        cached_titles = [os.path.splitext(file)[0] for file in files]
        return cached_titles

    def _cached_xml(self):
        """
        Return list of titles for which we have XML metadata files for in cache.
        """
        files = os.listdir(self.XML_FOLDER)
        cached_titles = [os.path.splitext(file)[0] for file in files]
        return cached_titles

    def _fetch_movie(self, title):
        """
        Download movie metadata fram imdb.com, save it as XML file in cache.
        title
            Title should be in IMDB's canonical format, eg. 'Dinosaur (2000)
        Returns imdb.Movie object, or None if no matches found.
        """
        parts = imdb.utils.analyze_title(title)
        movies = self.imdb_access.search_movie(parts['title'])
        if not len(movies) > 0:
            return None
        try:
            # Get first movie with matching year
            year = parts['year']
            for movie in movies:
                if movie['year'] == year:
                    break
        except KeyError:
            # No year?  Return first match
            movie = movies[0]

        # Load full set of data for movie
        self.imdb_access.update(movie)

        # Save movie metadata to XML file in cache
        path = self._generate_xml_path(title)
        self._save_xml(movie, path)
        return movie

    def _fetch_poster(self, title):
        """
        Download poster image from IMDB, save it in cache.
        """
        movie = self.get_movie(title)
        url = movie.get('full-size cover url') or movie.get('cover url')
        if url is None:
            return None

        # Download poster image
        response = urllib2.urlopen(url)
        data = response.read()
        # Save poster image
        path = self._generate_poster_path(title)
        fh = open(path, 'wb')
        fh.write(data)
        fh.close()
        return path

    def _generate_poster_path(self, title):
        """
        Return the path to the poster image for the movie.
        """
        file_name = title + '.jpg'
        file_path = os.path.join(self.POSTER_FOLDER, file_name)
        return file_path

    def _generate_xml_path(self, title):
        """
        Return the path to the XML file for the movie instance.
        """
        file_name = title + '.xml'
        file_path = os.path.join(self.XML_FOLDER, file_name)
        return file_path

    def _load_xml(self, path):
        """
        Load movie object from XML file with given path.
        """
        fh = open(path, 'rt')
        xml = fh.read()
        fh.close()
        movie = imdb.helpers.parseXML(xml)
        return movie

    def _save_xml(self, movie, path):
        """
        Save movie object to XML file to given path.
        """
        xml = movie.asXML()
        fh = open(path, 'wt')
        fh.write(xml)
        fh.close()
