"""I1 Visual grounding — locate objects in an image, return bbox/point/count in 0-1000 coords.
Industry pattern: open-vocabulary grounding (Grounding-DINO / OWL-ViT style), here run via
Muse's visual_grounding tool in the agent run, results stored in grounding-20261101.json.
Rule: grounding is evidence, not a label by itself — a bbox that touches an edge is a crop flag
for the QA gate, a count >1 for a unique room item is a duplication flag.
Verified runs in this job:
- angle-01: chair bbox 588,530-664,692; TV 136,463-263,691; window 623,301-762,532; coffee table 375,856-521,1000
- angle-06: pink wingback chair COUNT = 2, points (916,545) foreground right + (668,689) centre — DUPLICATE confirmed
- angle-10: TV 192,510-363,811; TV stand 187,797-384,1000 (stand bottom cropped at frame edge)
"""
import json, pathlib
GROUNDING = {
  "angle-01": {"chair": [588,530,664,692], "tv": [136,463,263,691], "window": [623,301,762,532], "coffee_table": [375,856,521,1000]},
  "angle-06": {"chair_count": 2, "chair_points": [[916,545],[668,689]]},
  "angle-10": {"tv": [192,510,363,811], "tv_stand": [187,797,384,1000]},
}
if __name__ == "__main__":
    print(json.dumps(GROUNDING, indent=2))
