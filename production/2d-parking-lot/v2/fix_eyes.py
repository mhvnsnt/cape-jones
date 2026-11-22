#!/usr/bin/env python3
"""fix_eyes.py — repair the 11 eye parts on branch v2-rig-parts.

Bug found 2026-11-22 (own-eyes on the re-rendered proofs): the separate eye
parts (330x82) render ~3.6x too big — giant white ovals sticking out past the
cowl ("white wings") + a faint grey guide line across the face. Measured:
- head part (180x240) already carries correctly-sized baked-in white eyes,
  centres (64.4,70.1)/(112.8,70.4), 48.4px apart;
- eye parts' white-eye centres (80.9,41.7)/(247.7,41.8), 166.9px apart;
- the anchor is EXACTLY right (eye-part centre -> sheet (1024,95) = the head's
  baked-eye midpoint (1023.6,95.25) from BOXES["head"] (935,25,1115,265)),
  so only the SCALE is wrong. placement() centres the part on the anchor by
  w/h at runtime, so scaling the PNGs fixes Blender + proof + cut at once.
Fix per part: scale 0.32x (0.29 exact + margin so the variant outline fully
covers the baked outline), recenter on its own eye-midpoint, zero alpha<128
(kills the semi-transparent grey guide line, alpha ~52).
Pupil parts: the "pupil" was a single black dot BETWEEN the eyes (not pupils
at all) and centre/audience were near-identical. Erase the central dot and
draw a proper black pupil inside EACH white eye: pupil_center at each eye's
centre; pupil_audience shifted down ~10px + inward ~5px in part coords (a
visible roll toward the viewer — direction choice, documented in CHECKPOINT).
Usage: python3 fix_eyes.py [--dry-run] — downloads from the branch, fixes in
memory, uploads back to the same paths (gh api, with existing blob sha).
"""
import cv2, numpy as np, subprocess, json, base64, sys

REPO = "mhvnsnt/cape-jones"
BRANCH = "v2-rig-parts"
BASE = "production/2d-parking-lot/v2/rig-parts"
EYES = ["eyes_white_default", "eyes_look_left", "eyes_look_up_b",
        "eyes_look_down", "eyes_look_up_c", "eyes_sideeye_a",
        "eyes_closed", "eyes_angry", "eyes_smug_sideeye",
        "eyes_pupil_center", "eyes_pupil_audience"]
SCALE = 0.32
DEFAULT_MID = (164.3, 41.8)   # white-eye midpoint, default/pupil parts
DEFAULT_DIST = 166.9

def gh(path, method="GET", data=None):
    cmd = ["gh", "api", f"repos/{REPO}/{path}"]
    if method == "PUT":
        cmd = ["gh", "api", "-X", "PUT", f"repos/{REPO}/{path}", "--input", "-"]
    r = subprocess.run(cmd, input=data, capture_output=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"gh {method} {path} failed: {r.stderr.decode()[:200]}")
    return r.stdout

def download(name):
    raw = gh(f"contents/{BASE}/{name}.png?ref={BRANCH}")
    content = json.loads(raw.decode())["content"]
    arr = np.frombuffer(base64.b64decode(content), dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    assert img is not None and img.shape[2] == 4, f"{name}: bad decode"
    return img

def white_eye_mid(img):
    """(midpoint, distance) of the two white-eye centroids, or defaults."""
    w = (img[:, :, 0] > 230) & (img[:, :, 1] > 230) & (img[:, :, 2] > 230) & (img[:, :, 3] > 200)
    ys, xs = np.where(w)
    if len(xs) < 200:
        return DEFAULT_MID, DEFAULT_DIST, False
    mid = (xs.min() + xs.max()) / 2.0
    L = xs < mid
    R = xs >= mid
    lc = (xs[L].mean(), ys[L].mean())
    rc = (xs[R].mean(), ys[R].mean())
    return ((lc[0] + rc[0]) / 2.0, (lc[1] + rc[1]) / 2.0), rc[0] - lc[0], True

def fix_pupils(img, audience=False):
    """Erase the central black dot; draw a pupil inside each white eye."""
    mid, _dist, _ok = white_eye_mid(img)
    # erase the central dot: black opaque px within r=26 of the image centre
    h, w = img.shape[:2]
    cx, cy = w / 2.0, h / 2.0
    yy, xx = np.mgrid[0:h, 0:w]
    dot = ((xx - cx) ** 2 + (yy - cy) ** 2 < 26 ** 2) & (img[:, :, 3] > 200) & \
          (img[:, :, 0] < 80) & (img[:, :, 1] < 80) & (img[:, :, 2] < 80)
    img[dot, 3] = 0
    # draw pupils at the white-eye centres (measured before the erase)
    wht = (img[:, :, 0] > 230) & (img[:, :, 1] > 230) & (img[:, :, 2] > 230) & (img[:, :, 3] > 200)
    ys, xs = np.where(wht)
    m = (xs.min() + xs.max()) / 2.0
    L = xs < m
    R = xs >= m
    centres = [(xs[L].mean(), ys[L].mean()), (xs[R].mean(), ys[R].mean())]
    for i, (px, py) in enumerate(centres):
        if audience:
            px += 5 if i == 0 else -5   # inward
            py += 10                    # down toward the viewer
        cv2.circle(img, (int(round(px)), int(round(py))), 14, (0, 0, 0, 255), -1, cv2.LINE_AA)
    return img

def process(name, img):
    mid, dist, measured = white_eye_mid(img)
    if name in ("eyes_pupil_center", "eyes_pupil_audience"):
        img = fix_pupils(img, audience=(name == "eyes_pupil_audience"))
        mid, dist, measured = white_eye_mid(img)
    # kill the faint guide line + soft fringe: zero alpha < 128
    img = img.copy()
    img[img[:, :, 3] < 128, 3] = 0
    # scale about the eye-midpoint, then recenter it on the new image centre
    small = cv2.resize(img, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
    nh, nw = small.shape[:2]
    smid = (mid[0] * SCALE, mid[1] * SCALE)
    centre = (nw / 2.0, nh / 2.0)
    dx, dy = int(round(centre[0] - smid[0])), int(round(centre[1] - smid[1]))
    out = np.zeros_like(small)
    sx0, sy0 = max(0, dx), max(0, dy)
    dx0, dy0 = max(0, -dx), max(0, -dy)
    wcopy = min(nw - sx0, nw - dx0)
    hcopy = min(nh - sy0, nh - dy0)
    if wcopy > 0 and hcopy > 0:
        out[sy0:sy0 + hcopy, sx0:sx0 + wcopy] = small[dy0:dy0 + hcopy, dx0:dx0 + wcopy]
    print(f"{name}: mid={mid[0]:.1f},{mid[1]:.1f} dist={dist:.1f} measured={measured} "
          f"-> {nw}x{nh} shift=({dx},{dy})", flush=True)
    return out

def upload(name, img):
    ok, buf = cv2.imencode(".png", img)
    assert ok
    data = buf.tobytes()
    path = f"{BASE}/{name}.png"
    for attempt in (1, 2, 3):
        # re-fetch the blob sha every attempt: a transient GET failure must not
        # poison all retries with a missing sha (PUT without sha on an existing
        # file -> HTTP 422).
        sha = None
        r = subprocess.run(["gh", "api", f"repos/{REPO}/contents/{path}?ref={BRANCH}"],
                           capture_output=True, timeout=60)
        if r.returncode == 0:
            sha = json.loads(r.stdout.decode()).get("sha")
        body = {"message": f"fix eye part scale 0.32x + guide-line removal ({name})",
                "content": base64.b64encode(data).decode(), "branch": BRANCH}
        if sha:
            body["sha"] = sha
        r = subprocess.run(["gh", "api", "-X", "PUT", f"repos/{REPO}/contents/{path}",
                            "--input", "-"], input=json.dumps(body).encode(),
                           capture_output=True, timeout=120)
        if r.returncode == 0:
            print(f"uploaded {path} ({len(data)} B)", flush=True)
            return True
        print(f"upload {name} attempt {attempt} FAILED: {r.stderr.decode()[:150]}", flush=True)
        import time
        time.sleep(5)
    return False

def main():
    dry = "--dry-run" in sys.argv
    for name in EYES:
        img = download(name)
        print(f"{name}: downloaded {img.shape[1]}x{img.shape[0]}", flush=True)
        if img.shape[1] < 150:
            # already fixed (originals are 305-335 wide, fixed are 98-107):
            # never scale twice.
            print(f"{name}: already fixed, skipping", flush=True)
            continue
        fixed = process(name, img)
        if dry:
            print(f"{name}: DRY RUN — not uploading", flush=True)
        else:
            assert upload(name, fixed), f"upload failed for {name}"
    print("ALL EYE PARTS FIXED", flush=True)

if __name__ == "__main__":
    main()
