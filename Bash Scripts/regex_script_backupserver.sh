#!/bin/bash

#Tjekker efter argument
if [ $# -ne 2 ]; then
    echo "Usage: $0 <date> <directory>"
    echo "Example: $0 2025-12-15 /home/ubunubackup/backups"
    exit 1
fi

#Command-line argumenter
DATE_PATTERN="$1"
SEARCH_DIR="$2"

#Regex mønster
REGEX=".*$DATE_PATTERN.*"

echo "Søger efter filer med datoen $DATE_PATTERN i $SEARCH_DIR ..."

#Looper igennem filer i stien (non-rekursivt)
for file in "$SEARCH_DIR"/*; do
    #Tjekker om det er en fil og ikke en sti
    if [[ -f "$file" && $(basename "$file") =~ $REGEX ]]; then
        echo "Found: $file"
    fi
done

