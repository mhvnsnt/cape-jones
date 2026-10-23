import json

cells = []

def md(src):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": src})

def code(src):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src})

md("""# Cape Jones EP — AI Watermark Removal v3 (LaMa)
Glyph-based detection (validated locally) + LaMa inpainting on GPU.
- RIGHT watermark box (720,1355) 300x90, LEFT watermark box (15,935) 300x90 — detect per frame via white-glyph scoring + whole-box-white guard (blocks the white-suit false positive).
- Bottom-right blur box (755,1735)-(1080,1920): filled on all non-card frames.
Outputs: test stills + cape-jones-v3-clean.mp4 in /kaggle/working.""")

code("""import torch, urllib.request, os
print('CUDA:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')
MODEL = '/kaggle/working/big-lama.pt'
if not os.path.exists(MODEL):
    urllib.request.urlretrieve('https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt', MODEL)
print('model MB:', os.path.getsize(MODEL) // 1048576)
""")

code("""import cv2, numpy as np, glob, os

IN = glob.glob('/kaggle/input/**/cape-jones-episode-v5.mp4', recursive=True)[0]
TPL_L = glob.glob('/kaggle/input/**/wm_template_left.png', recursive=True)[0]
TPL_R = glob.glob('/kaggle/input/**/wm_template_right.png', recursive=True)[0]
print('input:', IN)

def glyph_mask(tmpl_path, thresh):
    t = cv2.imread(tmpl_path)
    g = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.GaussianBlur(g, (0, 0), 6)
    return (g - bg) > thresh

LEFT_MASK = glyph_mask(TPL_L, 60)
RIGHT_MASK = glyph_mask(TPL_R, 40)
LEFT_BOX = (15, 935)
RIGHT_BOX = (720, 1355)
print('glyph px L/R:', int(LEFT_MASK.sum()), int(RIGHT_MASK.sum()))

def wm_present(frame, box, mask):
    x, y = box
    h, w = mask.shape
    roi = frame[y:y+h, x:x+w].astype(np.int32)
    mn = roi.min(axis=2); mx = roi.max(axis=2)
    white = (mn > 170) & ((mx - mn) < 45)
    return white[mask].mean() > 0.55 and white.mean() < 0.4

# Inpaint boxes (x1, y1, x2, y2) — widened to cover watermark glow (v3 test showed ghost past x=1030)
LEFT_INPAINT = (0, 920, 330, 1040)
RIGHT_INPAINT = (705, 1340, 1075, 1460)
# NO blur-box fill: v5 source is pre-blur (owner-verified); the corner is genuine footage.
""")

code("""import torch
_device = 'cuda' if torch.cuda.is_available() else 'cpu'
_model = torch.jit.load('/kaggle/working/big-lama.pt', map_location=_device)
_model.eval().to(_device)

def lama(patch_rgb, mask_u8):
    # patch_rgb: HxWx3 uint8 RGB; mask_u8: HxW uint8 (255 = inpaint)
    img = torch.from_numpy(patch_rgb).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    msk = torch.from_numpy((mask_u8 > 0).astype(np.float32)).unsqueeze(0).unsqueeze(0)
    H, W = patch_rgb.shape[:2]
    ph, pw = (8 - H % 8) % 8, (8 - W % 8) % 8
    if ph or pw:
        img = torch.nn.functional.pad(img, (0, pw, 0, ph), mode='reflect')
        msk = torch.nn.functional.pad(msk, (0, pw, 0, ph), mode='reflect')
    with torch.no_grad():
        out = _model(img.to(_device), msk.to(_device))
    out = out[0].permute(1, 2, 0).cpu().numpy()[:H, :W]
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)

print('LaMa ready on', _device)
""")

code("""# ---- TEST FRAMES FIRST: verify quality before trusting the full run ----
def inpaint_boxes(frame, boxes, ctx=110, feather=6):
    H, W = frame.shape[:2]
    out = frame.copy()
    for (x1, y1, x2, y2) in boxes:
        px1 = max(0, x1 - ctx); py1 = max(0, y1 - ctx)
        px2 = min(W, x2 + ctx); py2 = min(H, y2 + ctx)
        patch = out[py1:py2, px1:px2]
        pmask = np.zeros(patch.shape[:2], dtype=np.uint8)
        pmask[y1-py1:y2-py1, x1-px1:x2-px1] = 255
        res = lama(cv2.cvtColor(patch, cv2.COLOR_BGR2RGB), pmask)
        res = cv2.cvtColor(np.array(res), cv2.COLOR_RGB2BGR)
        if res.shape != patch.shape:
            res = cv2.resize(res, (patch.shape[1], patch.shape[0]))
        # paste the box area with a feathered edge so it fades into the background
        region = res[y1-py1:y2-py1, x1-px1:x2-px1].astype(np.float32)
        bh, bw = region.shape[:2]
        ay = np.ones(bh, dtype=np.float32); ax = np.ones(bw, dtype=np.float32)
        ay[:feather] = np.linspace(0, 1, feather); ay[-feather:] = np.linspace(1, 0, feather)
        ax[:feather] = np.linspace(0, 1, feather); ax[-feather:] = np.linspace(1, 0, feather)
        a = (ay[:, None] * ax[None, :])[:, :, None]
        orig = out[y1:y2, x1:x2].astype(np.float32)
        out[y1:y2, x1:x2] = (region * a + orig * (1 - a)).astype(np.uint8)
    return out

cap = cv2.VideoCapture(IN)
def frame_at(ms):
    cap.set(cv2.CAP_PROP_POS_MSEC, ms)
    r, f = cap.read()
    return f
tests = [(45000, [RIGHT_INPAINT], 'test-right45'),
         (89000, [LEFT_INPAINT], 'test-left89'),
         (10000, [], 'test-corner10-clean'),
         (83100, [RIGHT_INPAINT], 'test-magenta83')]
for ms, boxes, name in tests:
    f = frame_at(ms)
    res = inpaint_boxes(f, boxes)
    cv2.imwrite(f'/kaggle/working/{name}-lama.png', res)
    print('saved', name)
cap.release()
""")

code("""# ---- FULL PASS ----
import subprocess
cap = cv2.VideoCapture(IN)
fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
tmp = '/kaggle/working/v5-novid.mp4'
writer = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))
stats = {'left': 0, 'right': 0, 'blur': 0, 'frames': 0}
i = 0
while True:
    ret, frame = cap.read()
    if not ret: break
    boxes = []
    if wm_present(frame, LEFT_BOX, LEFT_MASK):
        boxes.append(LEFT_INPAINT); stats['left'] += 1
    if wm_present(frame, RIGHT_BOX, RIGHT_MASK):
        boxes.append(RIGHT_INPAINT); stats['right'] += 1
    if boxes:
        frame = inpaint_boxes(frame, boxes)
    writer.write(frame)
    i += 1
    if i % 300 == 0: print(f'{i}/{n}', stats, flush=True)
cap.release(); writer.release()
print('DONE', i, stats)
# Merge audio + final encode
r = subprocess.run(['ffmpeg', '-y', '-i', tmp, '-i', IN, '-map', '0:v:0', '-map', '1:a:0',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                    '/kaggle/working/cape-jones-v5-clean.mp4'], capture_output=True, text=True)
print('ffmpeg rc:', r.returncode, r.stderr[-300:] if r.returncode else 'ok')
""")

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3.10"}},
      "nbformat": 4, "nbformat_minor": 4}
out = '/home/hatch/workspace/viggle-inputs/wm-proper/cape-jones-wm-v3.ipynb'
with open(out, 'w') as f:
    json.dump(nb, f, indent=1)
print('wrote', out)
