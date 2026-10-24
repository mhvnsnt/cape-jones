#!/usr/bin/env bash
# re_push_tooncrafter.sh — helper for the ToonCrafter kernel re-push
# Run from the repo root after applying the v5 FP16 cell and kernel-metadata.json
set -e
cd "$(dirname "$0")/../../.."   # adjust if placed elsewhere
# Expected layout:
#   production/kaggle/tooncrafter/
#     cape_jones_tooncrafter_kaggle.ipynb
#     kernel-metadata.json
#     fp16_patch_cell_v5.py   (source for the non-fatal cell)

echo "=== ToonCrafter re-push checklist ==="
echo "1. Ensure kernel-metadata.json has dataset_sources populated."
echo "2. Ensure the notebook uses the non-fatal FP16 cell (see fp16_patch_cell_v5.py)."
echo "3. Internet ON, GPU T4, then:"
echo ""
echo "   cd production/kaggle/tooncrafter"
echo "   kaggle kernels push -p ."
echo ""
echo "4. After the run finishes, verify the Output tab has the MP4."
echo "   Quick Save does NOT capture /kaggle/working/ — use Save & Run All"
echo "   or the bulletproof saver cell."
echo ""
echo "Dataset slug currently expected: marsfmmg/tooncrafter-weights-fp16"
echo "(edit kernel-metadata.json if your actual dataset name differs)"
