#!/usr/bin/env python3

"""
Run the IMDb text file readers at full speed, without saving to database.
"""

import logging
import os
from pathlib import Path
import sys
from time import perf_counter


try:
    from cine import readers
except ImportError:
    # Add parent folder to import path
    sys.path.append(str(Path(__file__).parent.parent))
    from cine import readers


logger = logging.getLogger(__name__)


def print_row(*args):
    print("{:<16} {:>12} {:>12} {:>12}".format(*args))


def benchmark_reader(data_folder, reader_class):
    """
    Run a single reader.
    """
    reader = reader_class.from_folder(data_folder)
    start_time = perf_counter()
    count = 0
    for obj in reader:
        count += 1
    elapsed = perf_counter() - start_time
    per_sec = int(count // elapsed)

    # Report back
    fcount = f"{count:,}"
    felapsed = f"{elapsed:0.3f}s"
    fper_sec = f"{per_sec:,}"
    print_row(reader_class.__name__, fcount, felapsed, fper_sec)
    logging.info(
        "Read %s records from %r in %s. %s records per second.",
        fcount, reader_class.__name__, felapsed, fper_sec)
    return count


def benchmark_readers(data_folder, reader_classes):
    # Header
    width = 55
    separator = '=' * width
    print(separator)
    print_row('Class', 'Records', 'Seconds', 'Records/sec')
    print(separator)

    # Readers
    logging.critical("Starting IMDb reader benchmark")
    start_time = perf_counter()
    total_records = 0
    for reader_class in reader_classes:
        logger.debug("Reading data using the %s class", reader_class.__name__)
        total_records += benchmark_reader(data_folder, reader_class)
    elapsed_time = perf_counter() - start_time
    total_records_sec = int(total_records // elapsed_time)
    total_time = f"{elapsed_time:0.3f}s"
    logging.critical("Finished IMDb reader benchmark in %s", total_time)

    # Total
    print(separator)
    print_row('Totals', f'{total_records:,}', total_time, f'{total_records_sec:,}')
    print(separator)


readers = [
    readers.NameBasics,
    readers.TitleAkas,
    readers.TitleBasics,
    readers.TitleCrew,
    readers.TitleEpisodes,
    readers.TitlePrincipals,
    readers.TitleRatings,
]


def logging_setup(level):
    filename = Path(__file__).with_suffix('.log')
    logging.basicConfig(
        datefmt='%Y/%b/%d %H:%M:%S %z',
        filemode='w',
        filename=filename,
        format='[{asctime}] {levelname} {filename}:{lineno}: in {funcName}(): {message}',
        level=level,
        style='{',
    )


def main(folder):
    logger.debug("Looking for files in folder '%s'", folder)
    benchmark_readers(folder, readers)
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} DATA_FOLDER', file=sys.stderr)
        sys.exit(1)

    logging_setup(logging.INFO)
    folder = Path(sys.argv[1])
    folder = folder.expanduser().resolve()
    sys.exit(main(folder))
