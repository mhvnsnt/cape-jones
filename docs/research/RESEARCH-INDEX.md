# RESEARCH-INDEX.md — Master Research Index (Cape Jones)

Every research document in `docs/research/`, what it covered, what got pulled, what got wired, and what's still pending. Generated 2026-10-16.

## Pipeline / Production Docs

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| COMPLETE-PIPELINE.md | Full 12-stage pipeline | — | All 54 scripts in production/pipeline/ | — |
| FLIPACLIP-POST-PIPELINE.md | FlipaClip post stages | cleanup_lines.py, deghost.py | flipaclip_post.sh | — |
| LED-SCENE-ASSEMBLER.md | LED scene assembly | led_scene_assembler.py | Verified w/ contact sheets | Waiting on owner's 3 frames |

## Interpolation / Animation Research

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| INTERPOLATION-RESEARCH.md | RIFE vs alternatives | ToonCrafter (Kaggle) | kaggle_queue.py | ToonCrafter batch run (queued) |
| PRO-INBETWEENING-RESEARCH.md | Pro inbetweening | LayerInbetween (doc) | — | LayerInbetween pull (network failed) |
| TRACK-A-PULL.md | 17 interpolators, 8 rigging tools, VFX | trackA-ffmpeg-fx-chains.sh | trackA-wiring-guide.md | JoSTC, InterpAny-Clearer weights (Kaggle) |
| VECTOR-WORKFLOW.md | Raster→vector pipeline | raster_to_vector.py (vtracer) | — | — |

## AI Video / Generation Research

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| GEMINI-PULL.md | Wan 2.2, LTX-Video, ComfyUI, Cascadeur | wan2.2/, ltx-video/, comfyui/, cascadeur | Kaggle setup scripts | UE5 (30-40GB, pull when needed) |
| GEMINI-FULL-PULL.md | HunyuanVideo, Mochi, Krita AI Diffusion | hunyuanvideo/, mochi/, krita-ai-diffusion | — | Heavy weights on Kaggle |
| STUDIO-GRADE-PULL.md | One-to-All Animation (pose transfer), ToonComposer | one-to-all-animation/, tooncomposer/ | — | Kaggle T4 runbooks |
| 2026-STUDIO-DEEP-DIVE.md | ToonComposer 81-frame math, studio pipelines | tooncomposer/, OpenTimelineIO, AudioCraft | — | — |
| CONTINUED-PULL.md | html-animation, storyboard, explainroo, TheAnimeScripter | 7 tools + 4 scripts | Pipeline order documented | 3 failed clones (network) |
| EXPANSION-3.md | MMAudio, ChibiRigKit, Dia, OpenVoice, parler-tts, bark | 7 tools + 3 scripts | dialogue_pipeline.py, comp_glow.py, thumbnail_gen.py | TangoFlux (Kaggle-side) |
| EXPANSION-4.md | LayerInbetween, LTX-2.5, OmniColor, EverAnimate, OPEN-TOON | 6 tools + krita-batch-exporter | ffmpeg-animation-filters.sh | 4 failed pulls (network) |
| EXPANSION-5.md | Kandinsky 6.0, LuxTTS, lvsfunc, frei0r, SPAN | 4+9 pulls + 4 scripts | fx-particles.py, palette-enforce.py, cartoon-fx.sh | frei0r cmake build; SPAN weights (browser) |
| MEGA-PULL.md | Master synthesis of Tracks A–F | 19 pipeline scripts | All in production/pipeline/ | See track docs below |

## Mega-Pull Track Docs

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| TRACK-A-PULL.md | Animation/interp/rigging/VFX | 17 interpolators, 8 rigging, frei0r, manim | trackA-ffmpeg-fx-chains.sh + wiring guide | Weights on Kaggle |
| TRACK-B-AUDIO-PULL.md | 45 audio repos (18 TTS, VC, music, SFX) | tts_voices.py, voice_convert.py, music_gen.py, sfx_gen.py, stem_sep.py, audio_restore.py, lipsync_align.py | All 7 in production/pipeline/ | Model weights on Kaggle |
| TRACK-C-PULL-REPORT.md | 3D CC0 assets, game dev, comic/manga | Kenney Nature/Car kits, KayKit, ambientCG | In 3d-assets/ | itch.io rigged chars (browser) |
| TRACK-D-PULL.md | NLE, motion graphics, pre-pro | Kdenlive (pick), Motion Canvas, Trelby | kinetic_type.py, lower_thirds.py, fountain_to_beats.py, fountain_to_animatic.py, proxy_gen.py | — |
| TRACK-E-SUMMARY.md | Prod mgmt, distribution, localization | Kitsu+Zou, OpenCue, Flamenco | youtube_upload.py, metadata_gen.py, transcribe_translate.py, podcast_feed.py | — |
| TRACK-F-PULL.md | Merch, community, monetization, streaming | printful-mcp, ForgeBot, tip-root, OpenVT, Fanfare | merch_qr.py, obs_scene_json.py (this audit) | — |

## Audio / Voice Docs

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| SOUNDTRACKS.md | 3 official tracks | MP3s in cape-jones-build/ | finish.py --audio | — |
| COMPLEMENTARY-STACK.md | LatentSync, OpenFaceFX, MuseTalk, OpenMontage | LatentSync, OpenFaceFX, MuseTalk | — | LatentSync Kaggle notebook; OpenFaceFX .dat → Tahoma2D |

## Cloud / Devtools Research

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| CLOUD-RESEARCH.md | Cloud IDEs, free GPUs, browser 3D/video | OpenReel Video, video-ware | — | OpenCode (retry clone); Lightning AI signup (browser) |
| CLOUD-SERVICES.md | Service setup reference | — | docs/cloud/ | Colab Run All (browser); Codespace launch (browser) |
| docs/cloud/OPENCODE.md | OpenCode install guide | opencode/ source in production/devtools/ | — | — |
| docs/cloud/AIDER.md | Aider config | .aider.conf.yml | — | Gemini API key (browser) |
| docs/cloud/CODE-SERVER.md | code-server one-command install | — | Install on demand | — |
| docs/cloud/GEMINI-CLI.md | Gemini CLI free tier | — | Install on demand | — |

## Render Research

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| RENDER-SPEED.md | 4 speedup levers (~10-20x) | cycles_speed_config.py, render_half_interp.py, upscale_span.py | In production/pipeline/ | SPAN weights (browser); validate on 1 chunk |
| RENDER-2026-OPTIMAL.md | v4 notebook: no chunks, ~60min | gen_notebook_v4.py, render_parallel.py, merge_splits.py | kaggle_queue max_parallel | v4 untested on live Kaggle |

## Automation / Process Research

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| AUTOMATION.md | kaggle_queue.py GPU queue | kaggle_queue.py | systemd timer (15min) | Release queue when Pantera done |
| OVERNIGHT-PIPELINE.md | 30-min idle pipeline | cron job | Live, Step 1B friction-fixes | — |
| FRICTION-FIXES.md | 8 friction patterns → tools | research.py, checkpoint_audit.py, pull-to-repo.sh, Apprise notify() | All merged (PRs #28-30) | — |
| SMARTEN-UP.md | 8 recurring complaint patterns | 8 new laws in AGENTS.md | Propagated to configs | — |
| AGENT-UX-RESEARCH.md | Notifications, mobile control | Apprise 2.0.1 | notify() | Agent J (phone approvals) |
| AGENT-RELIABILITY-RESEARCH.md | Failure detection, checkpoints | checkpoint_audit.py | worker-watchdog (15min) | — |

## Studio / Technique Research

| Doc | Covers | Pulled | Wired | Pending |
|-----|--------|--------|-------|---------|
| 2026-PULL-SUMMARY.md | ToonCrafter, AnimeInbet, Chatterbox, Kokoro, Blender addons | tooncrafter/, kokoro-venv/ | KAGGLE-SETUP.md | Kokoro torch install (Kaggle) |
| 2026-STUDIO-DEEP-DIVE.md | (see AI Video above) | — | — | — |
| STUDIO-LEAKS.md | xSTUDIO, AL_USDMaya, Gazu, DJV | xstudio/, gazu (installed), djv | — | — |
| POST-INTERPOLATION.md | sketch-simplification, color-grade-ai | Both cloned | — | — |
| FULL-PRODUCTION-STACK.md | Zapsplat, Freesound, BBC SFX | — | Documented | — |
| VIDEO-MATTING.md | rembg/RVM matting | video-matte.py | Turnaround V2 used it | — |

## License Flags (documented, NOT pulled)

H3 (territorial exclusion — unusable US), TalkingPose/Wav2Lip/CDFI/XVFI/VFIformer (research-only), Fish/Breeze/F5-TTS/YuE2 (CC-BY-NC), Spine (paid), Remotion (paid teams), Blambot (NC), AGPL set (Kitsu/Zou, LibreTranslate, tip-root, Postiz — fine self-hosted). **Quaternius QAL v1.0 — OWNER APPROVED 2026-10-16.**
