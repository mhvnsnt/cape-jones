# TRACK F — Merchandise + Community + Monetization + Live Streaming

Open-source business-side tooling for a 2-person 2D animation show.
All cloned with `git clone --depth 1`. Nothing deployed — setup documented per repo.

**License legend:** ✅ permissive (MIT/BSD) · ⚠️ copyleft (GPL/AGPL — fine for
internal use; AGPL's network clause applies if you run it as a public service)
· ❌ no license file (all-rights-reserved by default — use as reference only).

---

## 1. Merchandise — `merch/`

| Tool | Path | What / why | License | Status | Size |
|---|---|---|---|---|---|
| printful-mcp | `merch/printful-mcp` | Printful print-on-demand: full Python API client (catalog, orders, mockup generator, shipping, webhooks) + MCP server + CLI. The POD backbone — browse products, generate mockups, place orders from scripts. | MIT ✅ | cloned | 1.6 MB |
| mockup-generator | `merch/mockup-generator` | Batch t-shirt mockup scripts (PIL compositing: displacement mapping, fabric texture, luminance-aware blending; batch artwork×tee runs; fabric swatches). Sparse checkout of `Scripts/` only — the 133 MB `Assets/` tee-photo templates were skipped (re-fetch from repo if needed). | ❌ none — reference only | cloned (scripts only) | 324 KB |
| segno | `merch/segno` | Best-in-class QR code lib (tiny, pure Python). Used by `glue/merch_qr.py` for merch-link QR codes on cards/posters/end-cards. | BSD-3 ✅ | cloned | 5.6 MB |

**Document-only (no clone needed):**
- **Printify API** — official REST API (developers.printify.com); Printful MCP above covers the same pattern. Pick one POD provider to start: Printful has the better API tooling here.
- **Pattern generators** — heropatterns.com (MIT SVG backgrounds) for merch pattern fills; `geopattern` (MIT) for generative geometric patterns. Both usable offline, no clone needed.
- **Price calculator** — none pulled; trivial spreadsheet math (base cost + markup). `monetization/creatoros` covers the revenue side.

---

## 2. Community — `community/`

| Tool | Path | What / why | License | Status | Size |
|---|---|---|---|---|---|
| ForgeBot | `community/forgebot` | Modular Discord bot framework (discord.py 2.4, SQLite, slash commands): moderation, tickets, economy, giveaways, AI chat. Drop a cog in `bot/cogs/` for show-specific commands (episode drops, character lore, poll-of-the-week). **Start here for the fan Discord.** | MIT ✅ | cloned | 212 KB |
| PaetreonLive | `community/paetreonlive` | Patreon `posts:publish` webhook → Discord announcement with keyword filter + role pings. Bridges Patreon and Discord with one tiny Python service. | ❌ none — reference only | cloned | 152 KB |

**Document-only (self-hosted, not deployed):**
- **Forums** — Flarum (MIT, flarum.org) = lightest modern forum, best 2-person pick. NodeBB (GPL-3.0) = heavier, real-time. Discourse (GPL-2.0) = most features, heaviest ops. Start with Discord; add Flarum only if the community outgrows it.
- **Fan art galleries** — Lychee (MIT, self-hosted photo gallery) for a fan-art wall; PhotoPrism (AGPL-3.0 ⚠️) if you want AI tagging.
- **Newsletter** — Listmonk (AGPL-3.0 ⚠️, single Go binary + Postgres) = the self-hosted Mailchimp. Keila (AGPL-3.0) = prettier UI, fewer features. **Or skip self-hosting:** newsy (GitHub-backed newsletter widget, free) turns a repo into a newsletter.
- **Polls/voting** — Framadate (AGPL ⚠️) for scheduling polls; in practice: Discord native polls + ForgeBot giveaway cogs cover 90% of show needs.
- **Publish-everywhere** — Markette (AGPL-3.0 ⚠️, `docker compose up`): write once → X/Bluesky/Threads/Mastodon/LinkedIn/FB/IG/YouTube/Reddit/Telegram/Discord + Listmonk newsletters. The 2-person social multiplier — worth evaluating before any manual cross-posting workflow.
- **Patreon-gated chat** — minionenjoyer/openchat: self-hosted chat with Patreon membership verification (OAuth gate, no credential retention). Interesting if you want supporter-only spaces without Discord.

---

## 3. Monetization — `monetization/`

| Tool | Path | What / why | License | Status | Size |
|---|---|---|---|---|---|
| threefive | `monetization/threefive` | SCTE-35 encode/decode (the ad-marker standard): parse ad cues from MPEGTS/HLS, inject markers, CLI + library. Relevant when you graduate to real broadcast/FAST-channel ad insertion. | GPL-2.0 ⚠️ | cloned | 1.1 MB |
| tip-root | `monetization/tip-root` | Self-hosted tipping platform: Go backend + Next.js frontend + Flutter app, **real-time OBS tip alerts via SSE**, Discord webhook notifications, QR tipping. Zero platform fees. (Removed the 60 MB prebuilt `Tip_Root.apk` from the working tree; it's in git history.) | AGPL-3.0 ⚠️ | cloned | 31 MB |
| creatoros | `monetization/creatoros` | Creator revenue dashboard (Next.js): YouTube Analytics API revenue tracking, sponsorship pipeline kanban, expense/tax tracker, video-level P&L, cash-flow calendar. Closest thing to the "sponsorship tracker → dashboard" ask. | ❌ none — reference only | cloned | 716 KB |

**Document-only:**
- **Analytics (privacy-friendly)** — Umami (MIT ✅, umami.is) = easiest self-hosted web analytics. Plausible (AGPL-3.0 ⚠️) = more mature, same idea. Either beats Google Analytics for a show site.
- **Stripe** — Payment Links need zero code for tips/merch pre-orders; full API via `stripe` pip package for webhooks. (His Stripe is already a connector.)
- **Ko-fi** — no public API; link-based donations + their Streamlabs/OBS alert integration. Use tip-root instead if you want self-hosted.
- **YouTube mid-roll** — set in YouTube Studio (monetization → ad breaks); API route is `liveBroadcasts` cuepoints for livestreams. threefive covers the broadcast-standard side.

---

## 4. Live streaming — `streaming/`

| Tool | Path | What / why | License | Status | Size |
|---|---|---|---|---|---|
| OpenSeeFace | `streaming/openseeface` | Open-source facial landmark tracking (ONNX, webcam → blendshape/pose data). The tracking engine under OpenVT, VSeeFace-via-Linux setups, burgertuber. BSD license, runs local. | BSD-2 ✅ | cloned | 161 MB (models) |
| OpenVT | `streaming/open-vt` | **The open VTube Studio alternative** (Godot, native Linux): Live2D tracking via OpenSeeFace, transparent window for OBS capture, VTS-compatible assets. The 2D-VTuber pick for character streams. | MIT ✅ | cloned | 38 MB |
| burgertuber | `streaming/burgertuber` | Minimal working example: three.js avatar + OpenSeeFace bridge + Twitch channel-point rewards. Best "how do I wire tracking to a web avatar" reference. | ❌ none — reference only | cloned | 24 MB |
| awesome-vtubing-on-linux | `streaming/awesome-vtubing-on-linux` | Curated list: OBS, v4l2loopback, Kalidoface, XR Animator, audio tools. The Linux VTuber landscape in one page. | ❌ (link list) | cloned | 128 KB |
| Fanfare | `streaming/fanfare` | **Self-hosted Streamlabs-style suite** (Bun, one process): alerts (follow/sub/tip/raid/merch/redemption), chat box, goal bars, loyalty points, polls, public tip page, Hype Train engine — all as OBS browser-source URLs. **Start here for stream overlays.** | MIT ✅ | cloned | 420 KB |
| CriStream | `streaming/cristream` | Self-hosted StreamElements/Nightbot alternative (Docker): Twitch bot (commands, timers, automod, loyalty, song requests), alert overlays with WYSIWYG editor, polls/predictions, Discord integration. Heavier than Fanfare; pick one. | MIT ✅ | cloned | 15 MB |
| obsws-python | `streaming/obsws-python` | Python client for OBS WebSocket v5 (port 4455). Script OBS: scene switching, source toggles, screenshots. Basis for automation glue. | GPL-3.0 ⚠️ | cloned | 372 KB |
| recbar | `streaming/recbar` | OBS recording companion bar: REC indicator, mic VU, chapter marks + markdown export, **window-based auto scene switching**, mobile remote. Small, focused, immediately useful while recording. | MIT ✅ | cloned | 524 KB |

**Document-only:**
- **SnenkBridge** (GPL-3.0 ⚠️, faeyumbrea/snenkbridge): iPhone → Live2D params → VTube Studio, cross-platform. Use if you go the VTube Studio (paid) route on Linux.
- **LilacVT** (erodozer/open-vt fork): adds VRM 3D avatars + bundled OpenSeeFace to OpenVT. Watch this if 3D avatars enter the picture.
- **OBS Advanced Scene Switcher** (GPL-2.0 ⚠️, Warmuptill/obs-advanced-scene-switcher): the macro/automation plugin for OBS — auto-switch on window, audio, time. Install as plugin, no code.
- **v4l2loopback** (GPL-2.0): Linux virtual camera kernel module — pipe OBS output to a fake webcam for Discord/Zoom.
- **Kalidoface** (web, kalidoface.com / 3d.kalidoface.com): zero-install browser VTuber (Live2D + VRM) via MediaPipe. Fastest path to test a VTuber segment with zero setup.
- **live2d.mk** (calamytryx): single-file browser Live2D stage + look-maker with webcam/OpenSeeFace tracking, usable as OBS browser source.

---

## Glue scripts — `glue/`

| Script | What |
|---|---|
| `glue/merch_qr.py` | QR code generator for merch/show links (PNG+SVG, print-ready). `pip install segno`, then `python3 merch_qr.py --out qr_out --link "Merch Store=https://..."`. ✅ tested |
| `glue/obs_scene_json.py` | Generates an importable OBS scene-collection JSON with browser-source slots (alerts/chat/goal/events) pointed at Fanfare URLs. Import via OBS → Scene Collection → Import. ✅ tested |

---

## Practical picks: next 3 months vs later

**Next 3 months (2-person team):**
1. **Fanfare** — stream alerts/overlays in one MIT-licensed Bun process. Cheapest path to professional-looking streams.
2. **ForgeBot** — fan Discord with show-specific cogs (episode pings, lore commands, giveaways).
3. **merch_qr.py + segno** — QR codes on every merch card/poster/end-card from day one.
4. **mockup-generator** — batch tee mockups for the first merch drop.
5. **printful-mcp** — POD pipeline without touching the Printful dashboard.
6. **recbar + obsws-python** — recording workflow automation.
7. **creatoros** (as reference) — sponsorship pipeline + revenue tracking shape; rebuild the parts you need or run it.
8. **Markette** (evaluate) — one write → every social + newsletter. Huge time saver for two people.

**Nice-to-have later:**
- OpenVT + OpenSeeFace VTuber rig for character-hosted streams (needs avatar art/rig first).
- tip-root self-hosted tipping (AGPL — fine for internal use; offer source per license).
- CriStream if Fanfare's bot features aren't enough.
- Listmonk newsletter once the list justifies it; Flarum forum once Discord overflows.
- threefive SCTE-35 only when broadcast/FAST distribution is real.
- Umami/Plausible analytics when the show site launches.
