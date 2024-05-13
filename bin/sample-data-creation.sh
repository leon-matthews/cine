#!/usr/bin/bash

set -o errexit
set -o nounset

#####################################################
# Create subset of IMDB data for testing purposes   #
#####################################################
# Sample files with the first and last NUM_ROWS     #
# lines of data. The output files are compressed,   #
# just like the originals, and have 2 * NUM_ROWS    #
# lines of data.                                    #
#####################################################

# Config ############################################
NUM_ROWS=10000                  # Rows per half
OUTPUT_FOLDER="../tests/data/"  # Relative to script file
#####################################################


# Number of arguments
if [ $# -eq 0 ]
then
    echo "Provide folder containing IMDB data files"
    echo "usage: $0 DATA_FOLDER"
    exit 1
fi

# Input folder?
INPUT_FOLDER="$1"
if [ ! -d "$INPUT_FOLDER" ]; then
    echo "Given location not a folder: $INPUT_FOLDER"
    exit 2
fi


# Output folder
SCRIPT_FOLDER="$( cd -- $(dirname "$0"); pwd -P)"
OUTPUT_FOLDER="$SCRIPT_FOLDER/$OUTPUT_FOLDER"
if [ ! -d "$OUTPUT_FOLDER" ]; then
    echo "Check config, output folder not found: $OUTPUT_FOLDER"
    exit 3
fi


# Create sample files!
cd $INPUT_FOLDER
for NAME in *.gz;
do
    echo "$NAME"
    zcat -d "$NAME" | (head -n $NUM_ROWS; tail -n $NUM_ROWS) | gzip --fast > "$OUTPUT_FOLDER$NAME"
done
