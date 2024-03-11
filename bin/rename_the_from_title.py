#!/usr/bin/env python3

"""
Rename movie files and movie folders, moving 'the' to the end.

eg.

"The Queen (2006)/The Queen (2006).ogm"

to

"Queen, The (2006)/Queen, The (2006).ogm"
"""

import glob
import os
import re
import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Rename movies to move 'The' to the end of the title")
        print('usage: {} folder', file=sys.stderr)
        raise SystemExit(1)

    folder = sys.argv[1]
    assert os.path.isdir(folder), 'Given path is not a folder'
    folder = os.path.abspath(folder)

    # Generate new folder name
    num_folders_renamed = 0
    num_files_renamed = 0
    for name in os.listdir(folder):
        new_name = re.sub(r'^(The) ([^(]*) (\(\d+\))$', r'\2, \1 \3', name)
        # Does folder need to renamed?
        if new_name == name:
            continue

        # Check contents
        path = os.path.join(folder, name)
        for f in glob.glob(os.path.join(path, name+'*')):
            movie_folder = os.path.dirname(f)
            file_name = os.path.basename(f)
            _, extension = os.path.splitext(file_name)
            from_path = os.path.join(movie_folder, file_name)
            to_path = os.path.join(movie_folder, "{}{}".format(new_name, extension))
            print(from_path)
            print(to_path)
            os.rename(from_path, to_path)
            num_files_renamed += 1

        new_path = os.path.abspath(os.path.join(folder, new_name))
        print(path)
        print(new_path)
        print()
        os.rename(path, new_path)
        num_folders_renamed += 1

    print()
    print("{:,} files renamed".format(num_files_renamed))
    print("{:,} folders renamed".format(num_folders_renamed))
