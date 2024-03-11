#!/usr/bin/env python3

import logging
import os
import sys

from db import db


# Configure global logger
logging.basicConfig(
    #~ format="%(asctime)s %(levelname)s %(name)s %(message)s",
    format="%(message)s",
    level=logging.INFO,
)


log = logging.getLogger(__name__)


if __name__ == '__main__':

    path_in = 'imdb.db'
    path_out = 'imdb-search.db'

    # Input database must already exist
    if not os.path.exists(path_in):
        log.error("Source database not found: {}".format(path_in))
        sys.exit(1)

    # Create search database, deleting existing
    if os.path.exists(path_out):
        log.info('Deleting existing search database')
        os.unlink(path_out)
    search_db = db.SearchDB(path_in, path_out)
    search_db.create()
