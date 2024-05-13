"""
Measure the speed/memory trade-off of enabling slots in record dataclasses.

Experiment to find the pros and cons of enabling slots for the reader
dataclasses, ie. ``@dataclass(slots=True)``. This is available only in
Python 3.10+

No slots:
    FINISHED 1,396,899 records in 6.637s
    Used 673.0MB of RAM, averaging 505 bytes per record

With slots:
    1,396,899 records in 7.659s
    Used 664.0MB of RAM, averaging 498 bytes per record

Use tuples instead of lists:
    1,396,899 records in 5.532s
    Used 567.2MB of RAM, averaging 426 bytes per record

Tuples AND slots:
    1,396,899 records in 2.890s
    Used 558.2MB of RAM, averaging 419 bytes per record

Something is wrong! That did practically nothing. Let's try and save memory
by other avenues. Maybe by using tuples instead of lists for the
embeded lists found in records.
"""

import logging
from pathlib import Path
import resource
import sys
import time


try:
    from cine import readers
except ImportError:
    # Add parent folder to import path
    sys.path.append(str(Path(__file__).parent.parent))
    from cine import readers


logger = logging.getLogger(__name__)


READERS = [
    readers.NameBasics,
    readers.TitleAkas,
    readers.TitleBasics,
    readers.TitleCrew,
    readers.TitleEpisodes,
    readers.TitlePrincipals,
    readers.TitleRatings,
]


def logging_setup(level):
    logging.basicConfig(level=level)


def main(data_folder: Path) -> int:
    """
    Create a huge list containing ALL of the records from ALL of the readers.
    """
    logger.info('STARTED')
    started = time.perf_counter()
    records = []
    for reader_class in READERS:
        logger.debug(reader_class.__name__)
        reader = reader_class.from_folder(data_folder)
        for record in reader:
            records.append(record)

    # Time
    elapsed = time.perf_counter() - started
    rate = len(records) / elapsed
    logger.info(f"FINISHED {len(records):,} records in {elapsed:.3f}s")

    # Memory
    bytes_ = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    bytes_per = round(bytes_ / len(records))
    megabytes = bytes_ / 1024 / 1024
    logger.info(f"Used {megabytes:.1f}MB of RAM, averaging {bytes_per} bytes per record")

    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} DATA_FOLDER', file=sys.stderr)
        sys.exit(1)

    logging_setup(logging.DEBUG)
    folder = Path(sys.argv[1]).expanduser().resolve()
    sys.exit(main(folder))
