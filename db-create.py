#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path
import sys

from cine.importer import Importer
from cine.utils import argparse_existing_folder

import builtins
from functools import partial
from pprint import pprint
builtins.pp = partial(pprint, sort_dicts=False)


# Configure global logger
logging.basicConfig(
    format="%(levelname)-7s %(message)s",
    level=logging.INFO,
)


logger = logging.getLogger(__name__)


def main(options: argparse.Namespace) -> None:
    importer = Importer(options.folder)


def parse(args: list[str]) -> argparse.Namespace:
    description = "Create database from IMDB data files"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'folder',
        default=Path.cwd(),
        metavar='FOLDER',
        type=argparse_existing_folder,
        help='folder containing IMDB data files',
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    code = 0
    options = parse(sys.argv[1:])
    try:
        main(options)
    except:
        code = 1
        raise
    sys.exit(code)
