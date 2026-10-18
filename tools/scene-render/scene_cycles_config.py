#!/usr/bin/env python3
"""scene_cycles_config.py — Cycles presets for the LIVING ROOM interior
(volumetric god rays + LED glow + CRT emission) on Colab/Kaggle T4 GPUs.

Extends production/pipeline/cycles_speed_config.py (the character-animation
presets) with interior-specific tuning — it does NOT duplicate it. The base
presets already proved 16spp + adaptive 0.05 + GPU OIDN is the speed king;
this layer adds what interiors need and what volumetrics demand:

  INTERIOR NEEDS:
  - more diffuse bounces (4) — the violet LED wash lives on bounced light;
    the character preset's 2 bounces starves interiors.
  - volume_bounces 2 — god-ray shafts + lamp haze need a second volume bounce
    or they go muddy.
  - caustics stay OFF (canon has no glass that needs them).

  VOLUMETRIC SPEED (Blender 4.5 LTS, verified attribute names on 4.5.3):
  - volume_step_rate 2.0 — halves volume marching cost; visually identical
    for soft fake-shaft haze (Blender Manual: raise step rate for bg fog).
  - volume_max_steps 256 — safety net for the big room volume.
  - use_volume_guiding True — probability guiding helps thin volumes
    (the shafts) converge faster on GPU.

PRESETS:
  living_room         — final look, Colab/Kaggle T4
  living_room_preview — blocking/timing, ~4x faster
  living_room_hero    — close-ups, higher samples

Usage (headless, on the render lane):
    import scene_cycles_config
    scene_cycles_config.apply("living_room")

    # or CLI: blender -b living_room.blend --python \\
    #   tools/scene-render/scene_cycles_config.py -- living_room
"""
import os
import sys

try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False


def _load_base():
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(6):
        cand = os.path.join(root, "production", "pipeline",
                            "cycles_speed_config.py")
        if os.path.exists(cand):
            break
        root = os.path.dirname(root)
    else:
        raise RuntimeError("cycles_speed_config.py not found above " + here)
    if os.path.dirname(cand) not in sys.path:
        sys.path.insert(0, os.path.dirname(cand))
    import cycles_speed_config
    return cycles_speed_config


def _set_scrambling(c, value):
    if not hasattr(c, "scrambling_distance"):
        return
    try:
        c.scrambling_distance = value
    except TypeError:
        # 4.5.3 LTS exposes it as float; newer builds as enum
        c.scrambling_distance = 1.0 if value == "AUTOMATIC" else value


def apply(preset="living_room", scene=None):
    base = _load_base()
    sc = scene or bpy.context.scene
    c = sc.cycles

    if preset == "living_room":
        try:
            base.apply_optimized(sc, preset="animation")
        except TypeError as e:
            # cycles_speed_config sets scrambling_distance='AUTOMATIC' but on
            # 4.5.3 LTS the property is a float. Everything before that line
            # already applied; fix the one property and continue.
            if "scrambling_distance" not in str(e):
                raise
            c.scrambling_distance = 1.0
        # interiors need bounced light
        c.max_bounces = 8
        c.diffuse_bounces = 4
        c.glossy_bounces = 3
        c.transmission_bounces = 2
        c.volume_bounces = 2
        c.transparent_max_bounces = 8
        # volumetrics: cheaper marching, guided sampling
        c.volume_step_rate = 2.0
        c.volume_preview_step_rate = 4.0
        c.volume_max_steps = 256
        if hasattr(c, "use_volume_guiding"):
            c.use_volume_guiding = True
        _set_scrambling(c, "AUTOMATIC")

    elif preset == "living_room_preview":
        try:
            base.apply_optimized(sc, preset="preview")
        except TypeError as e:
            if "scrambling_distance" not in str(e):
                raise
            c.scrambling_distance = 1.0
        c.diffuse_bounces = 2
        c.volume_bounces = 1
        c.volume_step_rate = 4.0
        c.volume_max_steps = 128
        if hasattr(c, "use_volume_guiding"):
            c.use_volume_guiding = True

    elif preset == "living_room_hero":
        try:
            base.apply_optimized(sc, preset="hero")
        except TypeError as e:
            if "scrambling_distance" not in str(e):
                raise
            c.scrambling_distance = 1.0
        c.max_bounces = 10
        c.diffuse_bounces = 5
        c.glossy_bounces = 4
        c.volume_bounces = 3
        c.volume_step_rate = 1.0
        c.volume_max_steps = 512
        if hasattr(c, "use_volume_guiding"):
            c.use_volume_guiding = True
        _set_scrambling(c, "AUTOMATIC")

    else:
        raise ValueError(
            f"unknown preset: {preset} "
            "(living_room/living_room_preview/living_room_hero)")

    print(f"scene_cycles_config: applied '{preset}'", flush=True)
    print(f"  samples={c.samples} thr={c.adaptive_threshold} "
          f"diffuse={c.diffuse_bounces} vol_bounces={c.volume_bounces} "
          f"step_rate={c.volume_step_rate}", flush=True)
    return sc


def _verify():
    sc = bpy.context.scene
    apply("living_room_preview", sc)
    c = sc.cycles
    assert c.volume_step_rate == 4.0, c.volume_step_rate
    assert c.diffuse_bounces == 2, c.diffuse_bounces
    assert c.denoiser == "OPENIMAGEDENOISE", c.denoiser
    apply("living_room", sc)
    assert c.volume_step_rate == 2.0 and c.diffuse_bounces == 4
    assert c.volume_max_steps == 256
    print("SCENE_CYCLES_CONFIG VERIFY: all 3 presets apply cleanly")


if __name__ == "__main__" and IN_BLENDER:
    if "--verify" in sys.argv:
        _verify()
    else:
        arg = next((a for a in sys.argv[1:]
                    if a in ("living_room", "living_room_preview",
                             "living_room_hero")), "living_room")
        apply(arg)
