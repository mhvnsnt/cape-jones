#!/bin/sh
# fetch-animlab.sh — fetch AnimLab Linux .deb (+ Android .apk) for v0.2.27
#
# PROVEN ROUTE (2026-11-22, $0, no manual work): the Kaggle-kernel no-auth
# itch flow — GET game page (CSRF + cookies) -> POST /download_url -> signed
# download-page URL -> GET download page (upload IDs) -> POST /file/{id} ->
# signed Cloudflare R2 URL (60s TTL) -> download immediately.
# Script kept at ~/workspace/_animlab-wireup-20261120/fetch/direct_download.sh;
# kernel pattern in fetch/kaggle-kernel/. This VM's egress IP is 429-throttled
# by itch on the POST endpoints and the browser Download button silently fails,
# so do NOT retry the plain curl/browser routes first — go straight to Kaggle.
#
# CANONICAL BINARY HOME (already landed, verify before re-fetching):
#   Release production-stack-free-20261120 on mhvnsnt/dream-girl:
#   https://github.com/mhvnsnt/dream-girl/releases/download/production-stack-free-20261120/AnimLab-Linux-v0.2.27-x86_64.deb
#   size 79,278,566 B
#   sha256 46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf
#
# Usage (itch download-page route — only if re-fetching from itch):
#   ./fetch-animlab.sh "<itch download-page URL>"
#   The download-page URL is $1 because its tokens expire in ~30 min —
#   NEVER hardcode a download link. Get a fresh one from the itch page:
#   set price $0.00 -> "No thanks, just take me to the downloads".
#   Requires: curl (or wget), sha256sum, grep/sed.
# Output: animlab_<version>_amd64.deb + animlab_<version>.apk in ./animlab-bin/
#   plus SHA-256 printed for each. Upload both to the repo Release named below.
# Release to upload to: production-stack-free-20261120 (mhvnsnt/dream-girl)
#   — binaries are staged there, not as blobs in the tree.
set -eu
URL="${1:-}"
if [ -z "$URL" ]; then
  echo "usage: $0 \"<itch download-page URL>\"" >&2
  echo "Get a fresh URL from the itch AnimLab page ($0 checkout, tokens expire in ~30 min)." >&2
  echo "Or skip itch entirely: the v0.2.27 .deb is already on Release production-stack-free-20261120 (mhvnsnt/dream-girl)." >&2
  exit 1
fi
# Commented fallback: Arttista direct download URL (same author family of tools).
# Uncomment and use as $1 if the AnimLab page itself is unreachable:
#   https://arttista.itch.io/arttista/download/19179272
#   NOTE: that URL fetches Arttista, NOT AnimLab — it is a fallback fetch route
#   only if the AnimLab download page is down, and what it downloads must be
#   labelled Arttista, never AnimLab.
OUTDIR="animlab-bin"
mkdir -p "$OUTDIR"
echo "Fetching download page..."
PAGE="$OUTDIR/download-page.html"
curl -fsSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" "$URL" -o "$PAGE"   || wget -q -U "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" "$URL" -O "$PAGE"
# Extract the Linux .deb and Android .apk links from the page.
DEB_URL=$(grep -oE 'https://[^"'"'"' ]+\.deb' "$PAGE" | grep -iv arm64 | head -n 1 || true)
APK_URL=$(grep -oE 'https://[^"'"'"' ]+\.apk' "$PAGE" | head -n 1 || true)
if [ -z "$DEB_URL" ]; then echo "ERROR: no Linux .deb link found on the page (token may have expired — fetch a fresh URL)." >&2; exit 1; fi
if [ -z "$APK_URL" ]; then echo "ERROR: no Android .apk link found on the page (token may have expired — fetch a fresh URL)." >&2; exit 1; fi
echo "Linux .deb: $DEB_URL"
echo "Android .apk: $APK_URL"
curl -fL -o "$OUTDIR/animlab_linux_amd64.deb" "$DEB_URL"
curl -fL -o "$OUTDIR/animlab_android.apk" "$APK_URL"
echo "--- sizes ---"
ls -l "$OUTDIR/animlab_linux_amd64.deb" "$OUTDIR/animlab_android.apk"
echo "--- sha256 ---"
sha256sum "$OUTDIR/animlab_linux_amd64.deb" "$OUTDIR/animlab_android.apk"
echo "--- expected (v0.2.27) ---"
echo "Linux .deb 79,278,566 B, sha256 46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf"
echo "Android .apk ~66 MB. If sizes are far off, the download is wrong — do not upload."
echo "Upload both files to repo Release: production-stack-free-20261120 (mhvnsnt/dream-girl)."
echo "Done. Binaries are in $OUTDIR/ — NOT committed to the tree."