from PIL import Image
import numpy as np

S1 = "/home/hatch/workspace/sitcanon-work/strips"
S2 = "/home/hatch/workspace/sitcanon-work/strips2"
T = np.asarray(Image.open(f"{S1}/strip_top.png").convert("RGB")).astype(np.float32)
M = np.asarray(Image.open(f"{S2}/ov_mid.png").convert("RGB")).astype(np.float32)
B = np.asarray(Image.open(f"{S2}/ov_bottom.png").convert("RGB")).astype(np.float32)

def content_rows(A):
    rm = A.mean(axis=(1, 2))
    idx = np.nonzero(rm > 2.0)[0]
    return int(idx.min()), int(idx.max())

for nm, A in (("strip_top", T), ("ov_mid", M), ("ov_bottom", B)):
    print(nm, "content rows:", content_rows(A))

def feather_into(out, upper, tag):
    lo_o, hi_o = content_rows(out)
    lo_u, hi_u = content_rows(upper)
    r0, r1 = max(lo_o, lo_u), min(hi_o, hi_u)
    print(f"{tag}: overlap rows {r0}..{r1} ({r1 - r0 + 1} rows)")
    assert r1 - r0 >= 10, "overlap too small"
    lower_overlap = out[r0:r1 + 1].copy()
    out[lo_u:hi_u + 1] = upper[lo_u:hi_u + 1]
    for r in range(r0, r1 + 1):
        a = (r - r0) / (r1 - r0)
        out[r] = lower_overlap[r - r0] * (1 - a) + upper[r] * a
    return out

out = T.copy()
out = feather_into(out, M, "top->ov_mid")
out = feather_into(out, B, "ov_mid->ov_bottom")

img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
p = "/home/hatch/workspace/your_files/final-repaired/FINAL_front_f40_v1.png"
img.save(p)
rm = np.asarray(img).astype(np.float32).mean(axis=(1, 2))
for b in (180, 360):
    print(f"row means r{b-4}-{b+4}:", np.round(rm[b - 4:b + 5], 1))
img.crop((0, 140, 960, 220)).resize((1920, 160), Image.LANCZOS).save("/tmp/seam1_big.png")
img.crop((0, 320, 960, 400)).resize((1920, 160), Image.LANCZOS).save("/tmp/seam2_big.png")
print("saved", p, img.size)
