# 2026-Level Tool Pull — Summary (2026-10-16)

## AI Cartoon Interpolation
| Tool | Status | Notes |
|------|--------|-------|
| **ToonCrafter** | ✅ Cloned + Kaggle guide | SIGGRAPH Asia 2024, trained on cartoons, 12GB VRAM → Kaggle T4 |
| **AnimeInbet** | ✅ Already present | ICCV 2023, vector-graph inbetweening, no ghosting by design |

## AI Voice / TTS
| Tool | Status | Notes |
|------|--------|-------|
| **Kokoro** | 🔄 Installing | 82M params, CPU-compatible, Apache-2.0 |
| **Chatterbox** | ✅ Cloned | Voice cloning, MIT, 23 languages |

## AI Auto-Coloring
| Tool | Status | Notes |
|------|--------|-------|
| **BasicPBC** | ✅ Cloned | CVPR 2024 paint-bucket colorization |

## Research
| Tool | Status | Notes |
|------|--------|-------|
| **Awesome-AI4Animation** | ✅ Cloned | ICCVW 2025 curated GenAI animation papers/models |

## Blender Addons
| Tool | Status | Notes |
|------|--------|-------|
| guided-tweening | ✅ Cloned | Stroke-by-stroke inbetweening hints (Blender 5) |
| smart2d | ✅ Cloned | Smart Bones (Blender 5.0+) |
| tiny-2d-rig | ✅ Cloned | Auto 2D rigging (Blender 4.3+) |

## Upscaling
| Tool | Status | Notes |
|------|--------|-------|
| RealESRGAN_x4plus_anime_6B | ✅ Downloaded (17.9MB) | Anime-specific 4x, BSD-3 |

## AI Music (documented, not pulled — GPU models)
- Stable Audio 3 (Stability AI, open-weight)
- Magenta Realtime 2 (Google, open-source)
- MiniMax Music 3.0 (open-weight, 08.2026)

## Key Insight
ToonCrafter is the game-changer: it's the first open-source interpolation
**specifically trained on cartoons** (not real video). This directly addresses
the RIFE ghosting problem on flat animation colors.
