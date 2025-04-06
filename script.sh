#!/bin/bash

DEST="$HOME/.config"

for item in *; do
    if [ -d "$item" ]; then
        echo "Copying $item to $DEST..."
        cp -r "$item" "$DEST/"
    fi
done
