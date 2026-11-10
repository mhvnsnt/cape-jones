# TRACK E — Production Management + Distribution + Localization

Pulled 2026-10-16. All in `~/workspace/tools/`. Glue scripts in
`~/workspace/tools/post-pipeline/` (see its README.md).
Disk: 85% at end of pull (started 81%; other parallel tracks also writing — my
track's footprint is ~620MB: ~459MB clones + 160MB venv). All clones
`--depth 1` with `.git` stripped after. pip cache purged.

## 1. Production management

| Tool | Path | Size | What / why | License | Status |
|---|---|---|---|---|
| Kitsu (self-hosted) | `tools/kitsu` + `tools/zou` | 15M + 26M | cgwire/kitsu (Vue frontend) + cgwire/zou (Python/Flask REST backend) — the animation-industry production tracker (shots, assets, tasks, statuses, review/playlists, quotas). Used by Blender Studio. Self-host via Docker (postgres + redis + minio). API + Gazu SDK (already had). | AGPL-3.0 ⚠️ (flag: ok internal, bad for SaaS) | cloned |
| OpenCue | `tools/opencue` | 178M | AcademySoftwareFoundation render-farm coordinator (Sony Imageworks' Cuebot). Python. Full farm queue/scheduling. | Apache-2.0 | cloned |
| Flamenco | `tools/flamenco` | 58M | Blender's own render manager (Manager + Worker + Blender add-on). Best fit for our Blender renders. | GPLv3+ | cloned |
| CGRU / Afanasy | `tools/cgru` | 42M | CGRU render farm suite (Afanasy scheduler). Lightweight, cross-platform. | LGPL-3.0 | cloned |
| OpenTimelineIO | (already had) | Editorial timeline interchange | Apache-2.0 | have |
| Blender Studio Pipeline | (already had) | Reference production pipeline | — | have |
| OpenProject | — | Full project mgmt (Gantt, agile). Heavy Rails+Angular. Documented, not cloned (disk). | GPLv3 | doc only |
| Taiga | — | Agile kanban/scrum, simple. kaleidos-ventures/taiga | MPL-2.0 | doc only |
| Leantime | — | Lightweight PM for small teams. | AGPL-3.0 ⚠️ | doc only |
| Tuleap | — | Agile/ALM suite. Enalean/tuleap | GPLv2 | doc only |

## 2. Distribution

| Tool | Path | Size | What / why | License | Status |
|---|---|---|---|---|---|
| youtube-upload | `tools/youtube-upload` | 92K | tokland CLI uploader (resumable). Wrapped by our `youtube_upload.py` (official API). | GPLv3 | cloned |
| yt-dlp | `tools/yt-dlp` | 15M | Download/backup/archive video (own uploads, references). | Public domain (Unlicense) | cloned |
| TubeArchivist | `tools/tubearchivist` | 8.5M | Self-hosted YouTube archive + local analytics of your channel. Docker. | GPLv3 | cloned |
| Postiz | — | — | Multi-platform scheduler (YT, TikTok, IG, FB, X, Threads, Bluesky). Docker self-host. | AGPL-3.0 ⚠️ | doc only |
| `youtube_upload.py` | `tools/post-pipeline/` | — | Official YouTube Data API v3 resumable uploader, reads metadata_gen.py sidecar. Needs one-time OAuth (`client_secrets.json`). | built | tested |
| `metadata_gen.py` | `tools/post-pipeline/` | — | Title/description/tags/chapters generator from `shows.json` + beats JSON. | built | tested |
| `podcast_feed.py` | `tools/post-pipeline/` | — | iTunes-compatible podcast RSS feed from episode manifest JSON. | built | tested |
| Thumbnail A/B | — | — | YouTube's built-in "Test & Compare" covers A/B natively; no OSS tool needed. | — | n/a |

## 3. Localization

| Tool | Path | Size | What / why | License | Status |
|---|---|---|---|---|---|
| Argos Translate | `tools/argos-translate` | 3.1M | Offline neural MT library (OpenNMT). Powers `--engine argos` in our script. | MIT | cloned |
| LibreTranslate | `tools/libretranslate` | 3.3M | Self-hosted translation API server. Powers `--engine libre`. | AGPL-3.0 ⚠️ | cloned |
| Aegisub | `tools/aegisub` | 32M | Subtitle editor (timing, typesetting, karaoke). Source pulled; needs build. | BSD-3-Clause | cloned |
| Subtitle Edit | `tools/subtitleedit` | 75M | Subtitle editor (C#/.NET). Source pulled; needs build. NOTE: pulled HEAD's LICENSE is MIT (relicensed upstream) — was historically GPLv3. | MIT (per pulled LICENSE) | cloned |
| pysubs2 | `tools/pysubs2` | 2.9M | Python subtitle parsing/editing library. | MIT | cloned |
| faster-whisper | system pip | — | Whisper transcription backend used by our script (already installed). | MIT | have |
| `transcribe_translate.py` | `tools/post-pipeline/` | — | faster-whisper → source SRT → translated SRTs (argos local / libre server); SRT shift/scale/VTT manager. Deps in `post-pipeline/venv` (srt installed; argos engine needs stanza+torch ~1GB — install manually when disk allows, see README). | built | built, argos engine pending torch |

## License flags (AGPL)
Kitsu, LibreTranslate, Leantime, Postiz are AGPL-3.0: fine for internal
self-hosted use; do NOT build a public SaaS on modified versions without
releasing source.

## Recommended stack for a 2-person animation team
- **Tracking:** Kitsu self-hosted (Docker) + Gazu for automation. It is the
  animation-industry standard; shot/asset statuses, review playlists, quotas.
- **Render queue:** Flamenco (native Blender; zero friction) — OpenCue only if
  the farm outgrows a few workers.
- **Distribution:** metadata_gen.py → youtube_upload.py (official API) per
  episode; TubeArchivist for channel archive/analytics; Postiz self-hosted for
  cross-platform scheduling (IG/TikTok/FB/X) once volume justifies it.
- **Localization:** transcribe_translate.py (faster-whisper + Argos offline)
  → SRT per language, upload as YouTube captions; Aegisub for hand-fixing
  timing/typesetting on dialogue-heavy episodes.
