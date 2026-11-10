#!/bin/bash
# pull-to-repo.sh — Pull a tool DIRECTLY into a repo checkout, wire it up, push.
# PULL-STRAIGHT-TO-STORE LAW: never stage on local disk when you can go direct.
#
# Usage:
#   pull-to-repo.sh <git-url> <repo-checkout-dir> <dest-subdir> [--branch BRANCH]
#
# Example:
#   pull-to-repo.sh https://github.com/user/tool.git \
#     ~/workspace/cape-jones-build/cape-jones tools/pulled/tool
#
# This clones directly into the repo working tree (not ~/workspace/tools/),
# so the tool is wired up in-place and ready to push via branch → PR → merge.

set -e

if [ $# -lt 3 ]; then
  echo "Usage: $0 <git-url> <repo-checkout-dir> <dest-subdir> [--branch BRANCH]"
  exit 1
fi

GIT_URL="$1"
REPO_DIR="$2"
DEST_SUBDIR="$3"
BRANCH=""

if [ "$4" = "--branch" ] && [ -n "$5" ]; then
  BRANCH="--branch $5 --single-branch"
fi

if [ ! -d "$REPO_DIR/.git" ]; then
  echo "ERROR: $REPO_DIR is not a git checkout" >&2
  exit 1
fi

DEST="$REPO_DIR/$DEST_SUBDIR"

if [ -e "$DEST" ]; then
  echo "ERROR: $DEST already exists — refusing to clobber" >&2
  exit 1
fi

echo "Cloning $GIT_URL directly into repo at $DEST_SUBDIR ..."
# shellcheck disable=SC2086
git clone --depth 1 $BRANCH "$GIT_URL" "$DEST"

# Strip .git so it becomes part of the parent repo, not a submodule
rm -rf "$DEST/.git"

echo "Done. Tool is at $DEST_SUBDIR inside $(basename "$REPO_DIR")."
echo "Next: wire it up, then branch → PR → merge."
echo ""
echo "Suggested:"
echo "  cd $REPO_DIR"
echo "  git checkout -b pull/$(basename "$DEST_SUBDIR")-$(date +%Y%m%d)"
echo "  git add $DEST_SUBDIR"
echo "  git commit -m \"Pull $(basename "$DEST_SUBDIR") into repo\""
