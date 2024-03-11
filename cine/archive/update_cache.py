#!/usr/bin/env python

"""
Manually populate metadata and cover images cache
"""

import os
import pprint
import sys

from cine.collection import Collection
from cine.metadata import Metadata

if __name__ == '__main__':

    movie_folders = ('/srv/movies/all', '/srv/movies2/all')
    c = Collection(*movie_folders)
    m = Metadata('/srv/movies/metadata')

    titles = c.get_titles()
    pprint.pprint(titles)
    print("{0} movie titles found".format(len(titles)))

    print "Testing mode...  Exiting without updating."
    sys.exit(1)

    # Delete superfluous cache entries
    excess = d.titles_excess(titles)
    if len(excess) > 100:
        print("I won't delete {0} cache entries!  Are you mad?".format(len(excess)))
        sys.exit(1)
    print("Deleting {0} excess cache entries...".format(len(excess)))
    for title in sorted(excess):
        print("Flushing excess cached entry for '{0}'".format(title))
        d.flush(title)

    # Create cache entries for missing titles
    missing = d.titles_missing(titles)
    print("Loading data for {0} missing cache entries...".format(len(missing)))
    for title in sorted(missing):
        print("  {0}".format(title))
        movie = d.get_movie(title)
        if not movie:
            print("    WARNING: movie data not found")
        image = d.get_poster(title)
        if not image:
            print("    WARNING: poster not found")
