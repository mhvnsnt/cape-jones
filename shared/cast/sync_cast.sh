#!/usr/bin/env bash
# Mirror the canonical cast manifest from western-heart into this repo (read-only copy; edit it in western-heart).
set -euo pipefail
gh api repos/mhvnsnt/western-heart/contents/shared/cast/cast.json -H 'Accept: application/vnd.github.raw' > shared/cast/cast.json
echo "synced $(python3 -c 'import json;print(json.load(open("shared/cast/cast.json"))["count"])') cast entries"
