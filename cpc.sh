#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "Usage: cpc <filename>"
    exit 1
fi

filename="$1"


if [ ! -f "$filename" ]; then
    echo "File '$filename' not found."
    exit 1
fi


if cat "$filename" | wl-copy; then
    echo "Copied:"
    cat "$filename"
else
    echo "Error: failed to copy to clipboard."
    exit 1
fi
