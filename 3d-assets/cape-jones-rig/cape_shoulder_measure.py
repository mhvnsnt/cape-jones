"""Measure body surface x-extent on the back (y>0.02) per z-band,
and trapezius top surface to fit the cape's pinned top."""
import bpy

body = bpy.data.objects['CapeJones_Body']
me = body.data
mw = body.matrix_world

print("BODY BACK x-extent (y>0.02) per z:")
for z0 in [0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.80]:
    xs = []
    for v in me.vertices:
        w = mw @ v.co
        if abs(w.z - z0) < 0.015 and w.y > 0.02:
            xs.append(w.x)
    if xs:
        print(f"  z={z0:.2f}: x in [{min(xs):.3f}, {max(xs):.3f}]  n={len(xs)}")

print("\nTRAPEZIUS top surface (max y where y>0) at |x|:")
for x0 in [0.0, 0.10, 0.15, 0.18, 0.20]:
    best = None
    for v in me.vertices:
        w = mw @ v.co
        if abs(abs(w.x) - x0) < 0.025 and 0.70 < w.z < 0.82 and w.y > 0:
            if best is None or w.y > best[0]:
                best = (w.y, w.z)
    if best:
        print(f"  |x|~{x0:.2f}: y={best[0]:.3f} z={best[1]:.3f}")
