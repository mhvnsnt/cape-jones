# Video Background Matting Tools

NO CHROMA KEY ON ANIMATION (owner law). These are AI-based tools that separate
characters from backgrounds without destroying white/colored characters.

## 1. RVM — Robust Video Matting (RECOMMENDED)

Real-time neural video matting with temporal consistency. True alpha mattes
with soft edges, not binary masks.

- **Location:** `~/workspace/tools/rvm/`
- **Model:** `models/rvm_mobilenetv3.pth` (15MB, 3.7M params)
- **Requires:** torch CPU (installed)
- **Usage:**
  ```python
  import torch, sys
  sys.path.insert(0, "~/workspace/tools/rvm")
  from model import MattingNetwork
  model = MattingNetwork("mobilenetv3")
  model.load_state_dict(torch.load("models/rvm_mobilenetv3.pth", map_location="cpu"))
  model.eval()
  rec = [None]*4
  with torch.no_grad():
      for frame in frames:  # (H,W,3) numpy uint8
          src = torch.from_numpy(frame).permute(2,0,1).unsqueeze(0).float()/255.
          fgr, pha, *rec = model(src, *rec, torch.tensor(1.0))
          # pha = alpha matte (0-1), fgr = foreground RGB
  ```
- **Speed:** ~17s/frame CPU @1080x1920. Downsample input for speed.
- **Repo:** https://github.com/PeterL1n/RobustVideoMatting

## 2. rembg per-frame (FAST, good enough for most)

AI segmentation per frame. Binary-ish masks, no temporal consistency,
but fast and handles white-on-white correctly.

- **Script:** `~/workspace/tools/video-matte.py`
- **Usage:** `video-matte.py input.mp4 --background bg.png --output out.mp4 [--fps 15] [--model u2netp]`
- **Models:** u2netp (portrait, fast, cached), u2net_human_seg (better, slower)
- **Speed:** ~15s/frame CPU @1080x1920

## 3. BackgroundMattingV2 (not yet pulled)

Needs a clean background plate + torch. Better quality than RVM when you
have a static background. Pull if RVM/rembg aren't enough.
https://github.com/PeterL1n/BackgroundMattingV2

## Test results (2026-10-15)

On `cape-jones-turnaround-v1.mp4` (white suit on white bg):
- colorkey: FAILED (destroyed white suit) — banned by owner law
- rembg u2netp: WORKS, clean separation, white suit intact
- RVM mobilenetv3: WORKS, true alpha mattes, soft edges
- Output: `~/workspace/cape-jones-build/turnaround-ai-matte.mp4`
