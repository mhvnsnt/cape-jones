"""Ep1 Scene 1 -- LED gag (production script, tools-side).
LEDStripMat currently has NO emission channel (Principled BSDF, dark gray base).
This script gives it one: Emission Color = canon violet #731AE5, and keys
Emission Strength @30fps:
  f0-29   steady 1.0 (Cape settles in)
  f30-41  flicker: 1.0, 0.1, 1.0, 0.2, 1.0, 0.1, 1.0 (the gag -- played straight)
  f42-89  slow pulse 0.7..1.0 (sine)
  f90-104 dropout 0.05 (he notices, does NOT fix it)
  f105+   steady 1.0
Single shared material => all three strips animate together (matches the gag:
the whole room's LEDs flicker, not one strip).
Run: blender -b living_room.blend --python led_gag.py  (then save or render).
Prints the keyed values as numeric proof.
"""
import bpy, math
m = bpy.data.materials['LEDStripMat']
bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
# sRGB #731AE5 -> linear
bsdf.inputs['Emission Color'].default_value = (0.175, 0.010, 0.785, 1.0)
strength = bsdf.inputs['Emission Strength']
keys = {}
for f in range(0, 30): keys[f] = 1.0
flick = [1.0, 0.1, 1.0, 0.2, 1.0, 0.1, 1.0]
for i, v in enumerate(flick): keys[30 + i * 2] = v
for f in range(42, 90): keys[f] = 0.85 + 0.15 * math.sin((f - 42) / 47 * math.pi * 2)
for f in range(90, 105): keys[f] = 0.05
for f in range(105, 130): keys[f] = 1.0
for f, v in keys.items():
    strength.default_value = v
    strength.keyframe_insert(data_path="default_value", frame=f)
print("LED_GAG keys:", {f: round(v, 2) for f, v in keys.items() if f in (0, 30, 32, 34, 36, 38, 40, 50, 65, 90, 100, 105)})
print("LED_GAG done: frames", min(keys), "-", max(keys))
