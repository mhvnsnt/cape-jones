#!/usr/bin/env bash
# Fetch the full commercial-grade tooling releases (with binary assets the
# GitHub connector cannot carry) and verify their sha256 hashes.
# The text sources are already vendored in tools/; this script gets the
# complete release zips (COA icons, Wiggle Bones images) for a full install.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p .downloads

fetch() { # $1 url, $2 file, $3 sha256
  local url="$1" file="$2" sha="$3"
  if [ -f ".downloads/$file" ]; then
    echo "already have $file"
  else
    curl -L --fail -o ".downloads/$file" "$url"
  fi
  echo "$sha  .downloads/$file" | sha256sum -c -
}

fetch "https://github.com/Aodaruma/coa_tools2/releases/download/v2.3.0/coa_tools2.zip" \
  "coa_tools2-v2.3.0.zip" \
  "5719aa99d7257ddd931979371459a6221cb9e651dc434f7863b833a31deae66d"

fetch "https://github.com/shteeve3d/blender-wiggle-2/releases/download/v2.2.3/wiggle_2.py" \
  "wiggle_2-v2.2.3.py" \
  "570ae0a1a17800ba13f38f8bfdae4068d4c0b88dad237f4a0f32237d6b9ab21e"

fetch "https://github.com/Hans-xwh/wiggle-bones/archive/refs/heads/main.zip" \
  "wiggle-bones-main.zip" \
  "75789f3186db47778e04dea93b3c500bc6f2f79a46a1611daa4b26a07cac3167"

echo "All three downloads verified. Install:"
echo "  COA Tools 2: unzip coa_tools2-v2.3.0.zip into Blender's addons dir"
echo "  Wiggle 2:    rename wiggle_2-v2.2.3.py -> wiggle_2.py, then install"
echo "  Wiggle Bones: unzip, install src/wiggle_bones/ as an addon"
echo "See tools/README.md for the Blender 5.0.1 notes."
