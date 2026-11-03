import subprocess, json, base64, os, sys
REPO = "mhvnsnt/cape-jones"
BR = "cape-jones-hallway-parody-20261102"
CJDIR = os.path.expanduser('~/workspace/_cj-dance-v2/build/parts')
WORK = os.path.expanduser('~/workspace/_hallway_study')

def gh_api(method, path, payload=None):
    cmd = ["gh", "api", "--method", method, path]
    inp = None
    if payload is not None:
        inp = json.dumps(payload); cmd += ["--input", "-"]
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        print("API FAIL", method, path, r.stderr[:800]); sys.exit(1)
    return json.loads(r.stdout) if r.stdout.strip() else {}

def land(mp4, sheet_bytes, verdict):
    main_sha = gh_api("GET", f"repos/{REPO}/git/ref/heads/main")["object"]["sha"]
    base_tree = gh_api("GET", f"repos/{REPO}/git/commits/{main_sha}")["tree"]["sha"]
    print("main:", main_sha, flush=True)
    files = []  # (repo_path, bytes)
    files.append(("production/dance-choreo/parody/cape-jones-hallway-parody-20261102.mp4", mp4))
    files.append(("production/dance-choreo/parody/cape-jones-hallway-parody-sheet-20261102.png", sheet_bytes))
    for f in ["layer_head.png","layer_torso.png","layer_arm_l.png","layer_arm_r.png","layer_leg_l.png",
              "layer_leg_r.png","layer_cape.png","layer_sock_l.png","layer_sock_r.png","pivots.json"]:
        files.append((f"production/dance-choreo/parody/cj_puppet/{f}", open(os.path.join(CJDIR, f), "rb").read()))
    puppet = {
        "name": "Cape Jones hallway puppet (assembled from _cj-dance-v2/build/parts)",
        "canvas": [1198, 1111],
        "feet_anchor": [599, 1111],
        "pivots_file": "pivots.json",
        "slots_order_back_to_front": ["cape", "leg_l", "leg_r", "torso", "arm_l", "arm_r", "head"],
        "layers": {"cape": "layer_cape.png", "leg_l": "layer_leg_l.png", "leg_r": "layer_leg_r.png",
                   "torso": "layer_torso.png", "arm_l": "layer_arm_l.png", "arm_r": "layer_arm_r.png",
                   "head": "layer_head.png", "sock_l": "layer_sock_l.png", "sock_r": "layer_sock_r.png"},
        "unused_in_build": ["sock_l", "sock_r (shoulder-height overlays in the source layers; not placed)"],
        "canon": {"suit": "white", "cowl": "#3E1473", "skin": "#E5B28C", "cape": "#000000"},
    }
    files.append(("production/dance-choreo/parody/cj_puppet/puppet.json", json.dumps(puppet, indent=1).encode()))
    files.append(("production/dance-choreo/parody/build_parody.py", open(os.path.join(WORK, "build_parody.py"), "rb").read()))
    files.append(("production/dance-choreo/parody/land_parody.py", open(os.path.join(WORK, "lander.py"), "rb").read()))
    readme = f"""# Cape Jones hallway parody — GB214 "The Words" Sc057 + Sc059

Cape Jones placed in Darwin's hallway dance slot, driven by the extracted
choreography (`../dance-gumball-darwin-words-sc057-sc059.json` + `../hallway-study-data.json`).
1920x1080, 25 fps, 303 frames (Sc057 198 + Sc059 105), production audio
(audio057 under Sc057, audio059 under Sc059, trimmed to frame durations).
MP4 is fragmented-MP4 (empty_moov) because this build lane encodes to a pipe;
it plays in browsers/players as-is and can be faststart-remuxed losslessly.
(Recovery build: encoded per scene to pipes — each scene blob persisted to
GitHub the moment it finished, after two runs were killed by VM reboots —
then joined with the ffmpeg concat demuxer, stream copy, no re-encode.)

## What drove each Cape Jones part
- **Root (position/scale):** Darwin's orange-pixel bbox measured per frame from
  the HD renders — bottom-center = feet anchor, bbox height = CJ figure height,
  sampled on twos. Sc057 height grows {verdict['h057_first']}px -> {verdict['h057_last']}px across the shot.
- **Head:** Darwin's head-comp keyframes — rotation from the matrix (atan2(b,a)),
  scale (relative, exponent 0.55), tx/ty normalized around the track median.
- **Legs:** Darwin's leg symbol keyframes (Layer 22 / Layer 23) — rotation from
  symbol matrices where a symbol instance exists, held pose-to-pose. In Sc057
  the clean-leg symbol track is sparse (the wide-shot legs were hand-drawn), so
  a bbox-aspect spread (measured bbox width/height) fills the stride there.
- **Torso:** lean derived from the extracted head-comp rotation (x0.35) plus
  root-velocity tilt. Derived, not a separate Darwin torso track.
- **Arms — GAP:** no fin/arm symbol track exists on either main puppet timeline
  (Sc057/Sc059 arms are hand-drawn 'rough arms' shape passes with no per-part
  transform to extract; the rough shapes' signal was not usable as a rotation
  track in this build). CJ's arms ride the torso and counter-rotate from the
  extracted head-comp rotation. This is derived coupling, NOT extracted arm
  choreography — named here as the build's biggest honest gap.
- **Cape — PROCEDURAL (disclosed):** Darwin has no cape; his tail was never
  placed in these puppets. CJ's cape is a pendulum lagging the root track's
  horizontal velocity. The one procedural piece in the build.
- **Flip / twist (Sc059):** both Darwin placements are flipped (negative a) and
  CJ is mirrored to match. In the twist (f43-97), CJ's whole-figure scaleX
  follows the measured bbox aspect vs its wind-up baseline; at the deepest
  squash (<0.5) he mirrors — a back-view suggestion. **GAP: CJ has no back-view
  head** (the source swaps in a drawn back-view head fragment); the front head
  is kept, mirrored.
- **Darwin removal:** orange mask (R>200, 90<G<190, B<90) dilated, plus green-shoe
  and median-difference pixels inside his expanded bbox (extended below the bbox,
  where his green shoes hang). Sc057: masked pixels are inpainted from the frame
  itself per frame (Telea). RECOVERY ITERATION: the first build filled Sc057 from
  the temporal median, but visual QA of that build proved the median itself is a
  Darwin ghost (he occupies the dance zone in most samples) and it smeared orange
  around CJ while his shoes survived below the bbox — the fill was changed to
  inpaint and the plate region extended downward; the median is kept only as a
  difference reference. Sc059's Darwin never leaves his area, so his plate is the
  temporal median with his union mask inpainted once (Telea) — sound there
  because inpaint discards the median inside the union. Head-symbol rotations
  beyond +/-90 deg in the source track (the symbol's back-view flips, atan2
  ~ +/-180) are folded to the equivalent near-level tilt — CJ has no back-view
  head (same gap as the Sc059 twist); the first build applied them raw and CJ
  tumbled upside-down at the Sc057 finale. Onlookers, crowd, hallway and
  framecounter stay because the plates are built from the frames themselves.

## Verification (numeric, this lane cannot write local media files)
- Distinct (head, leg_l, leg_r) poses across 303 frames: {verdict['distinct_poses']}
- CJ skin-tone pixels present in every frame where the source dancer is on screen (min per frame): {verdict['skin_px_min']} — {verdict['empty_frames']} Sc059 entry frames have no Darwin in the source at all (he enters from off-screen right), so those frames are the clean plate with no CJ, by design.
- Max residual Darwin-orange pixels in any cleaned plate: {verdict['orange_plate_max']}
- Max residual shoe-green pixels in any Sc057 plate region: {verdict['green_plate_max']} (new metric from the recovery iteration; the first build never measured the shoes)
- MP4 bytes: {verdict['mp4_bytes']} · Contact sheet: `cape-jones-hallway-parody-sheet-20261102.png` (9 frames)
- Full per-frame stats were printed by the build run and are summarized in the PR body.

## Puppet
`cj_puppet/` — the working Cape Jones puppet as used: full-canvas part layers
(1198x1111, alpha respected; transparent pixels carry white RGB but alpha 0),
`pivots.json`, and `puppet.json` (slots, anchor, canon colours). Sock layers are
included for completeness; they sit at shoulder height in the source art and
were not placed in this build.
"""
    files.append(("production/dance-choreo/parody/README.md", readme.encode()))
    entries = []
    for repo_path, data in files:
        blob = gh_api("POST", f"repos/{REPO}/git/blobs", {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        print("blob", repo_path, blob["sha"], len(data), flush=True)
        entries.append({"path": repo_path, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    tree = gh_api("POST", f"repos/{REPO}/git/trees", {"base_tree": base_tree, "tree": entries})
    commit = gh_api("POST", f"repos/{REPO}/git/commits", {
        "message": "Hallway parody: Cape Jones in Darwin's dance slot (Sc057+Sc059)\n\nCJ driven by extracted choreography: orange-bbox root, head-comp head,\nleg-symbol legs; arms derived (no fin track exists), cape procedural\n(disclosed). Darwin removed via orange mask + temporal median/inpaint.",
        "tree": tree["sha"], "parents": [main_sha]})
    gh_api("POST", f"repos/{REPO}/git/refs", {"ref": f"refs/heads/{BR}", "sha": commit["sha"]})
    pr = gh_api("POST", f"repos/{REPO}/pulls", {
        "title": "Hallway parody: Cape Jones in Darwin's hallway dance (Sc057+Sc059)",
        "head": BR, "base": "main",
        "body": f"Phase 2 build against STUDY-hallway-scene.md. CJ replaces Darwin in the hallway dance; onlookers/crowd/hallway/audio stay (plates built from the HD frames themselves).\n\n**Per-part drivers:** root = measured orange bbox (twos); head = head-comp keyframes; legs = leg symbol keyframes (+bbox-aspect spread in Sc057); torso = derived lean; **arms = GAP** (no fin track on main timelines — rough hand-drawn arms only; arms ride torso, counter-rotating from head-comp); **cape = procedural** pendulum (disclosed); Sc059 twist = measured bbox-aspect squash + mirror at deepest squash (**gap: no CJ back-view head**).\n\n**Verification (numeric — this lane's shell cannot persist media files locally, so the MP4/sheet exist in this PR; contact sheet included for eyeballing):** distinct poses {verdict['distinct_poses']}; CJ skin px min/frame (dancer-present frames) {verdict['skin_px_min']}; {verdict['empty_frames']} source frames contain no Darwin (Sc059 entry, off-screen) and carry no CJ; max residual orange in plates {verdict['orange_plate_max']}; Sc057 CJ height {verdict['h057_first']}->{verdict['h057_last']}px; MP4 {verdict['mp4_bytes']} bytes, 303 frames, 1920x1080/25fps, fragmented MP4 (pipe encode).\n\nAdditions only, zero deletions."})
    print("PR:", pr["number"], pr["html_url"], flush=True)
    pr_files = gh_api("GET", f"repos/{REPO}/pulls/{pr['number']}/files?per_page=100")
    for f in pr_files:
        print("PR file:", f["filename"], f["status"], f"+{f['additions']}/-{f['deletions']}", flush=True)
    assert all(f["deletions"] == 0 for f in pr_files), "deletions present!"
    merged = gh_api("PUT", f"repos/{REPO}/pulls/{pr['number']}/merge",
                    {"merge_method": "merge", "commit_title": f"Merge pull request #{pr['number']} from mhvnsnt/{BR}"})
    print("MERGED:", merged.get("merged"), merged.get("sha"), flush=True)
    print("PR_NUMBER", pr["number"], flush=True)
