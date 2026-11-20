#!/usr/bin/env bash
# fetch-verify.sh — pull all 10 Harmony + free-stack tools from the two
# releases on mhvnsnt/dream-girl, verify size + SHA-256, and skip any
# binary that is already on disk and verified (no re-download).
#
#   Harmony release:    harmony-equivalents-20261120 (id 452975939)
#   Free-stack release: production-stack-free-20261120 (id 452720539)
#
# Usage:
#   bash tools/free-stack/fetch-verify.sh [DEST_DIR] [all|harmony|free]
#   DEST_DIR defaults to ./tools-bin (next to the repo root when run from
#   the repo root; pass an explicit dir otherwise).
#   Second arg selects a subset; default is all 10 tools.
#
# Requirements: gh (authenticated), sha256sum, stat. No purchases, no
# accounts, no card — every asset here is a free release download.
# Exit non-zero if any download or verification fails; already-verified
# files are skipped, never re-downloaded.
set -euo pipefail

REPO="mhvnsnt/dream-girl"
HARMONY_REL="harmony-equivalents-20261120"
FREE_REL="production-stack-free-20261120"
DEST="${1:-./tools-bin}"
ONLY="${2:-all}"

# asset | release | size (bytes) | sha256
TOOLS_HARMONY=(
  "SynfigStudio-1.5.5-linux64.appimage|$HARMONY_REL|115539968|b85aabc26f690a0c150d2143c656c17f358b73abbedf8d01007f15a7a95740e9"
  "glaxnimate-x86_64.AppImage|$HARMONY_REL|182682816|e0f39cf67b79e80cdbbe8b3d858cab8a7b142e1c17f5944eb09af55fbc4a6347"
  "enve.AppImage|$HARMONY_REL|150658760|00b7081f0dfb8545c6eee31034407305cf63c630a002bd391fa1504eab01b1c0"
  "Wick.Editor-1.19.0.AppImage|$HARMONY_REL|216087317|92ff24c6f162e0144108d6dd47bf5f6d6ca6972d405c21b73c6da3a7d35f059b"
)
TOOLS_FREE=(
  "anicraft-0.2.1-linux-x86_64.AppImage|$FREE_REL|19024376|352456384d1e82f373d836dcbcd9f1473b1603c5c9c7b185d763218470091b31"
  "pencil2d-linux-amd64-v0.7.2.AppImage|$FREE_REL|60471800|4034b036258b6a13d4540911ebce085f31ee18a9dacf438845ac71998d42ff91"
  "Rigby2D_0.5.1_amd64.AppImage|$FREE_REL|96979448|27afa7de71a43e2fe45f27e605176a62b9a559db4b7f5f00f3a105870bdbd6ee"
  "Olive-8ac191ce-Linux-x86_64.AppImage|$FREE_REL|154107880|30a6c0d18dfb4ff77addd06984348656fd69d153cfa913eb3cde56a60aa14160"
  "kdenlive-26.08.3-x86_64.AppImage|$FREE_REL|214346232|2c8322edfc86605e4c98a78a019310d9b4fc46bb8e94e6fe313dc7dd987e7671"
  "browser-download-20261120T160026.367892390Z-0-douga-windows.zip|$FREE_REL|3766009|bf3bd41c5593736caf4b7d74ebcf4c00c52766691c3596f3d3c7b34a9ea0b774"
)

mkdir -p "$DEST"

verify_one() {
  local file="$1" want_size="$2" want_sha="$3"
  [ -f "$file" ] || return 1
  local got_size got_sha
  got_size="$(stat -c%s "$file")"
  [ "$got_size" = "$want_size" ] || return 1
  got_sha="$(sha256sum "$file" | awk '{print $1}')"
  [ "$got_sha" = "$want_sha" ] || return 1
  return 0
}

fetch_one() {
  local asset="$1" rel="$2" size="$3" sha="$4"
  local file="$DEST/$asset"
  if verify_one "$file" "$size" "$sha"; then
    echo "SKIP (already verified): $asset  $size B  sha256 ok"
    return 0
  fi
  echo "FETCH: $asset  ($rel, $size B)"
  # Remove a stale/partial copy before downloading, so a bad file can
  # never pass as verified.
  rm -f "$file"
  gh release download "$rel" --repo "$REPO" --pattern "$asset" --dir "$DEST"
  if verify_one "$file" "$size" "$sha"; then
    echo "OK: $asset  $size B  sha256 ok"
  else
    echo "FAIL: $asset — size/sha256 mismatch after download (expected $size B / $sha)" >&2
    return 1
  fi
}

case "$ONLY" in
  all)     LIST=("${TOOLS_HARMONY[@]}" "${TOOLS_FREE[@]}") ;;
  harmony) LIST=("${TOOLS_HARMONY[@]}") ;;
  free)    LIST=("${TOOLS_FREE[@]}") ;;
  *) echo "usage: $0 [DEST_DIR] [all|harmony|free]" >&2; exit 2 ;;
esac

fail=0
for entry in "${LIST[@]}"; do
  IFS='|' read -r asset rel size sha <<< "$entry"
  fetch_one "$asset" "$rel" "$size" "$sha" || fail=1
done

if [ "$fail" -eq 0 ]; then
  echo "ALL VERIFIED: ${#LIST[@]} tool(s) in $DEST"
else
  echo "FETCH-VERIFY FAILED — see FAIL lines above" >&2
  exit 1
fi
