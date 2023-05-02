#!/bin/bash

# Set the directory to start the search from
DIR="."

# Find all compressed files recursively in the directory
FILES=$(find "$DIR" -type f -name '*.tar.gz' -o -name '*.tgz' -o -name '*.tar.bz2' -o -name '*.tbz2' -o -name '*.tar.xz' -o -name '*.txz' -o -name '*.zip')

# Loop through the files and extract them
for FILE in $FILES; do
    echo "Extracting $FILE"
    tar -xf "$FILE"
done
