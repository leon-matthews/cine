"""
Provides an interface to the physical movie collection.
"""

import logging
import os
import re

from . import util

class Collection(object):
    """
    Read access to collection data.

    Iterates over collection, fetches metadata for individual titles, and
    compares collections.

    A collection is simply a file system tree of folders and files following
    the naming conventions outlined below:

    1. Every movie in collection is in its own folder.
    2. Each folder will also (eventually) contain metadata files from
       cine itself, eg. 'folder.jpg', 'metadata.xml', and 'about.mpg'.
    3. Folders may contain any number of other miscellaneous files such as
       subtitles, extras, etc... which are ignored by cine.
    4. The actual movie file is identified by its name, which should be in
       the cannonical IMDB format, plus its extension,
       eg. 'How to Train Your Dragon (2010).webm'
    5. There are no restrictions on folder names, but the usual convention
       is to always create folders using the IMDB name, then sometimes to
       group those folders inside another folder, to collection trilogies
       together, etc...

    A warning will be logged if exactly one movie file, as identified by its
    naming convention, is not found inside each movie folder.
    """
    def __init__(self, root, *roots):
        """
        Initialise reader with one or more root directories.

        eg.
        r = Reader('/srv/movies')
        r = Reader('/srv/movies01', '/srv/movies02', '/media/movies')
        """
        self.roots = tuple([root] + list(roots))
        for root in self.roots:
            if not os.path.isdir(root):
                raise ValueError("Collection root missing: '{0}'".format(root))
        self._titles = None

    def get_folder(self, title):
        """
        Return full path of an existing titles's folder.

        title
            Title in IMDB cannonical format, eg. 'Blade Runner (1982)'

        Raises an KeyError if title not found in collection.
        """
        title = util.clean_title(title)
        titles = self.get_titles()
        try:
            path = titles[title]
        except KeyError as e:
            e.args = ("Title not found: '{0}'".format(title),)
            raise e
        return os.path.dirname(path)

    def calculate_folder(self, title):
        """
        Calculates folder for new title, and returns its full path.

        title
            Title in IMDB cannonical format, eg. 'TRON (1982)'

        To avoid title folder double-ups, always check for an existing
        folder using `get_folder` first.  While this method always returns a
        valid folder for a given title, multiple roots and the presence of
        grouping folders mean a single title has many possible legal folders.

        * Uses the first collection root if more than one root in use.
        * Raises ValueError if title does not match expected format.
        * Does not create folder.
        """
        title = util.clean_title(title)
        root = self.roots[0]
        folder = os.path.join(root, title)
        return folder

    def get_titles(self):
        """
        Return dictionary mapping title to full path of main file.
        """
        # Lazy loading
        if self._titles is None:
            titles = {}
            for root in self.roots:
                for path, folders, files in os.walk(root):
                    for f in files:
                        try:
                            title = util.clean_title(f)
                        except ValueError:
                            pass
                        else:
                            titles[title] = os.path.abspath(os.path.join(path, f))
                self._titles = titles
        return self._titles
