"""Lane 3 audit part 4: are finger chains spatially contiguous? Which mesh finger is each chain at?"""
import bpy, numpy as np

rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]

def W(name):
    b = rig.pose.bones[name]
    return np.array(rig.matrix_world @ b.head, dtype=np.float64), np.array(rig.matrix_world @ b.tail, dtype=np.float64)

for side in ("L", "R"):
    print(f"=== hand_{side} ===")
    for f in ("index", "middle", "ring", "pinky"):
        segs = [f"finger_{f}_{i}_{side}" for i in (1, 2, 3)]
        pts = [W(s) for s in segs]
        gaps = []
        for i in range(2):
            gaps.append(np.linalg.norm(pts[i][1] - pts[i+1][0]))
        lens = [round(np.linalg.norm(h - t), 4) for h, t in pts]
        print(f"  {f}: seg_len={lens} chain_gaps(tail->next head)={[round(g,4) for g in gaps]}")
    for f in ("thumb",):
        segs = [f"finger_{f}_{i}_{side}" for i in (1, 2)]
        pts = [W(s) for s in segs]
        gap = np.linalg.norm(pts[0][1] - pts[1][0])
        lens = [round(np.linalg.norm(h - t), 4) for h, t in pts]
        print(f"  {f}: seg_len={lens} gap={round(gap,4)}")
    # inter-finger spacing: distance between chain midlines (base of finger 1)
    bases = {}
    for f in ("index", "middle", "ring", "pinky", "thumb"):
        h, _ = W(f"finger_{f}_1_{side}")
        bases[f] = h
    print("  base positions (x,y,z):")
    for f, p in bases.items():
        print(f"    {f}: {[round(v,3) for v in p]}")
