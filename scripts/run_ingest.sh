#! /bin/bash

DIR="$HOME/Downloads/MemoryCache"
inotifywait -m -e close_write -e moved_to "$DIR" | while read path action file; do
    fullPath="$path$file"
    fileSize=$(stat -c%s "$fullPath")
    if [[ "$file" != *.part ]] && [[ $fileSize -gt 0 ]]; then
        echo "Ingest triggered by '$file' ($fileSize bytes)."
        python3 ingest.py
    fi
done
