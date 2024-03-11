#!/bin/bash

if (( $# < 1 )); then
    echo "Create imdb test file from the head, middle, and tail of the" >&2
    echo "input file.  One thousand lines of each are concatenated" >&2
    echo "together to create the test file." >&2
    echo "" >&2
    echo "Will create .gz compressed files in the current directory" >&2
    echo "" >&2
    echo "usage: $0 <path>" >&2
    exit 1
fi

# Calculate file data
FILE_PATH="$1"
FILE_NAME=$(basename "$FILE_PATH")
EXTENSION=${FILE_NAME##*.}
if [ $EXTENSION != 'gz' ]; then
    echo "$0: error: input file should be gzip'd" >&2
    exit 1
fi
NUM_LINES=$( gzip -dc "$FILE_PATH" | wc -l )
NUM_LINES=$( echo $NUM_LINES | cut -d" " -f1 )
echo $NUM_LINES

# Degenerate case, whole file already short
if (( $NUM_LINES < 5000 )); then
    echo "Copying whole file, already small"
    cp "$FILE_PATH" "$FILE_NAME"
    if [ $EXTENSION != 'gz' ]; then
        gzip --best "$FILE_NAME"
    fi
    exit 0
fi

# Create temp file
TEMP_PATH=$( mktemp --tmpdir=. )
echo $TEMP_PATH

# Add content
echo "Add first 1000 lines..."
gzip -dc "$FILE_PATH" | head -n 1000 >> "$TEMP_PATH"

echo "Add middle 1000 lines..."
START=$[$NUM_LINES/2-500]
gzip -dc "$FILE_PATH" | head -n $START | tail -n 1000 >> "$TEMP_PATH"

echo "Add last 1000 lines..."
gzip -dc "$FILE_PATH" | tail -n 1000 >> "$TEMP_PATH"

# Movie into place, compress
gzip --best -c "$TEMP_PATH" > "$FILE_NAME"
chmod 664 "$FILE_NAME"
rm -f "$TEMP_PATH"
echo "Finished"

