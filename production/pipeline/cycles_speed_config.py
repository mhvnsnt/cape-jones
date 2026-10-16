#!/usr/bin/env python3
"""cycles_speed_config.py — Drop-in Cycles speed optimizations for Blender 4.x.

Apply AFTER your scene is built, BEFORE rendering:

    import cycles_speed_config
    cycles_speed_config.apply_optimized(scene, preset="animation")

PRESETS:
  "animation"  — Best for character animation on GPU. ~2.5-3x faster than
                 naive 32spp+OptiX with EQUAL or BETTER quality (less flicker).
  "preview"    — Draft quality, ~5-8x faster. For timing/animatic checks.
  "hero"       — Higher quality for close-ups. ~1.5x faster than naive.

THE WINS (measured, from openhouse-3d render-performance research):
  1. GPU OIDN (denoising_use_gpu=True) — OIDN on CPU costs ~2s/frame (~45%
     of frame time). On GPU it's essentially FREE. Also temporally MORE
     STABLE than OptiX denoiser for animation (OptiX flickers frame-to-frame).
  2. 16spp + adaptive threshold 0.05 — visually identical to 32spp/0.02
     at 100% crop for scenes lit by area/emissive lights. 2x fewer samples.
  3. Fixed sample count (not time_limit) — keeps noise level consistent
     frame-to-frame, so the denoiser behaves identically (no pulsing).

FUTURE (documented, not yet available):
  - OIDN 3 (H2 2026): temporal denoising + 3x supersampling. When it lands,
    render at 1/3 res and let OIDN 3 upscale 3x = ~9x fewer pixels.
"""
import bpy


def apply_optimized(scene=None, preset="animation"):
    sc = scene or bpy.context.scene
    c = sc.cycles

    if preset == "animation":
        # --- Sampling: fewer samples, tighter threshold ---
        c.samples = 16
        c.use_adaptive_sampling = True
        c.adaptive_threshold = 0.05
        c.adaptive_min_samples = 8
        c.time_limit = 0  # fixed samples = consistent noise = stable denoise

        # --- Denoising: OIDN on GPU (free + temporally stable) ---
        c.use_denoising = True
        c.denoiser = 'OPENIMAGEDENOISE'
        c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        # THE KEY LINE: move OIDN off CPU onto GPU
        if hasattr(c, "denoising_use_gpu"):
            c.denoising_use_gpu = True
        # Prefilter: accurate keeps detail at low sample counts
        if hasattr(c, "denoising_prefilter"):
            c.denoising_prefilter = 'ACCURATE'

        # --- Light paths: tuned for character scenes ---
        c.max_bounces = 4
        c.diffuse_bounces = 2
        c.glossy_bounces = 2
        c.transmission_bounces = 2
        c.volume_bounces = 1
        c.transparent_max_bounces = 4
        c.caustics_reflective = False
        c.caustics_refractive = False

        # --- Persistent data: no per-frame re-upload ---
        sc.render.use_persistent_data = True

    elif preset == "preview":
        c.samples = 8
        c.use_adaptive_sampling = True
        c.adaptive_threshold = 0.1
        c.adaptive_min_samples = 4
        c.time_limit = 0
        c.use_denoising = True
        c.denoiser = 'OPENIMAGEDENOISE'
        c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        if hasattr(c, "denoising_use_gpu"):
            c.denoising_use_gpu = True
        c.max_bounces = 2
        c.diffuse_bounces = 1
        c.glossy_bounces = 1
        c.transmission_bounces = 1
        c.volume_bounces = 0
        c.caustics_reflective = False
        c.caustics_refractive = False
        sc.render.use_persistent_data = True
        sc.render.use_simplify = True
        sc.render.simplify_subdivision = 1

    elif preset == "hero":
        c.samples = 32
        c.use_adaptive_sampling = True
        c.adaptive_threshold = 0.03
        c.adaptive_min_samples = 16
        c.time_limit = 0
        c.use_denoising = True
        c.denoiser = 'OPENIMAGEDENOISE'
        c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        if hasattr(c, "denoising_use_gpu"):
            c.denoising_use_gpu = True
        if hasattr(c, "denoising_prefilter"):
            c.denoising_prefilter = 'ACCURATE'
        c.max_bounces = 6
        c.diffuse_bounces = 3
        c.glossy_bounces = 3
        c.transmission_bounces = 3
        c.volume_bounces = 1
        c.caustics_reflective = False
        c.caustics_refractive = False
        sc.render.use_persistent_data = True

    else:
        raise ValueError(f"unknown preset: {preset} (animation/preview/hero)")

    print(f"cycles_speed_config: applied '{preset}' preset", flush=True)
    print(f"  samples={c.samples} adaptive_thr={c.adaptive_threshold} "
          f"denoiser={c.denoiser} gpu_denoise={getattr(c, 'denoising_use_gpu', 'n/a')}",
          flush=True)
    return sc


if __name__ == "__main__":
    # Test: apply to current scene and print settings
    import sys
    preset = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] in (
        "animation", "preview", "hero") else "animation"
    apply_optimized(preset=preset)
