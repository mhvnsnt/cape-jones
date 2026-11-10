#!/bin/bash
cd $(dirname $0)
echo "Removing quarantine from AnimeEffects"
xattr -d com.apple.quarantine AnimeEffects.app/
echo "Done, attempting run..."
open AnimeEffects.app
