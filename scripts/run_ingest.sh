#! /bin/bash

DIR="$HOME/Downloads/MemoryCache"
inotifywait -m -e create -e attrib "$DIR" | while read path action file; do  
    echo "The file '$file' appeared in directory '$path'"
    python3 ingest.py
done
