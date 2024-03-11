#!/usr/bin/python3

"""
Put each file in the given directory into its own folder.

The name of the folder is the same as the file, sans extension.
"""

import os
import sys


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Put each bare folder into its own folder, sans extension')
        print('usage: {} folder', file=sys.stderr)
        raise SystemExit(1)

    folder = sys.argv[1]
    assert os.path.isdir(folder), 'Given path is not a folder'
    folder = os.path.abspath(folder)

    num_folders = 0
    num_folders_created = 0
    num_files = 0
    num_files_moved = 0
    for file_name in os.listdir(folder):
        path = os.path.join(folder, file_name)
        if os.path.isdir(path):
            num_folders += 1
            continue

        num_files += 1
        folder_name, _ = os.path.splitext(file_name)

        output_folder = os.path.join(folder, folder_name)
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        num_folders_created += 1
        os.rename(path, os.path.join(output_folder, file_name))
        print("Moved: '{}'".format(file_name))

    print("{:,} folders detected".format(num_folders))
    print("{:,} folders created".format(num_folders_created))
    print("{:,} bare files dectected".format(num_files))
    print("{:,} files moved".format(num_files_moved))
