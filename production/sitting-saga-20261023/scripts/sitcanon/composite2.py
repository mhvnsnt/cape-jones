from PIL import Image
import numpy as np

d = "/home/hatch/workspace/sitcanon-work/strips2"
B = np.asarray(Image.open(f"{d}/ov_bottom.png").convert("RGB")).astype(np.float32)
M = np.asarray(Image.open(f"{d}/ov_mid.png").convert("RGB")).astype(np.float32)
T = np.asarray(Image.open(f"{d}/ov_top.png").convert("RGB")).astype(np.float32)

def content_rows(A):
    rm = A.mean(axis=(1, 2))
    idx = np.nonzero(rm > 2.0)[0]
    return idx.min(), idx.max()

for nm, A in (("bottom", B), ("mid", M), ("top", T)):
    print(nm, "content rows:", content_rows(A))

out = B.copy()

def feather_into(out, upper, tag):
    lo_b, hi_b = content_rows(out)
    lo_u, hi_u = content_rows(upper)
    r0, r1 = max(lo_b, lo_u), min(hi_b, hi_u)
    print(f"{tag}: overlap rows {r0}..{r1}")
    assert r1 - r0 > 30, "overlap too small"
    for r in range(r0, r1 + 1):
        a = (r - r0) / (r1 - r0)
        out[r] = out[r] * (1 - a) + upper[r] * a
    # extend content upward: rows the upper strip covers but out doesn't yet
    for r in range(lo_u, lo_b):
        out[r] = upper[r]
    return out

out = feather_into(out, M, "bottom->mid")
out = feather_into(out, T, "mid->top")

img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
p = "/home/hatch/workspace/your_files/final-repaired/FINAL_front_f40_v1.png"
img.save(p)
rm = np.asarray(img).astype(np.float32).mean(axis=(1, 2))
for b in (180, 360):
    print(f"row means r{b-4}-{b+4}:", np.round(rm[b - 4:b + 5], 1))
img.crop((0, 140, 960, 220)).resize((1920, 160), Image.LANCZOS).save("/tmp/seam1_big.png")
img.crop((0, 320, 960, 400)).resize((1920, 160), Image.LANCZOS).save("/tmp/seam2_big.png")
print("saved", p, img.size)
