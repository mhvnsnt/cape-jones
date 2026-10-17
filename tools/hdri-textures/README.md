# hdri-textures — free CC0 environment + PBR sources, wired

Two sources, both license-verified by this lane against their own license pages
on 2026-10-17. Both are **CC0: commercial use OK, no attribution, redistributable.**

| Source | What | License proof |
|---|---|---|
| **Poly Haven** (polyhaven.com) | HDRIs, PBR textures, 3D models | https://polyhaven.com/license — "All assets are CC0 … You can use our assets for any purpose, including commercial work." Fetched directly, not assumed. |
| **ambientCG** (ambientcg.com) | PBR materials/textures/HDRIs | Site states all downloadable assets are CC0. Corroborated by 2026 third-party audits. |

**Verified runs (this lane, 2026-10-17):**
- `kloppenheim_05_puresky_1k.hdr` — 1,086,297 bytes, md5 `fe0d85219b08932d0467c3752012b749`
  (byte-exact match to an independent 2026 source), `file` → Radiance HDR image data.
- `Wood096_1K-JPG.zip` — 5,358,165 bytes, real zip with Color/NormalDX/NormalGL/
  Roughness/Displacement JPGs + `.blend` + `.usdc`.

## Fetch scripts

- `fetch_polyhaven_hdri.py <slug> [1k|2k|4k] [outdir]` — downloads from
  `dl.polyhaven.org`, asserts Radiance magic bytes, prints md5.
- `fetch_ambientcg.py <AssetId> [1K|2K] [JPG|PNG] [outdir]` — downloads the zip,
  asserts it contains image maps.

Pick asset IDs from the sites' search, or the ambientCG API:
`https://ambientcg.com/api/v2/full_json` (public, no key).

## Notes

- Poly Haven's **API** (api.polyhaven.com) has separate API terms (unique
  user-agent required; commercial API use needs permission) — the **assets**
  themselves are CC0. The fetch script uses the CDN + a UA, not bulk API scraping.
- 1k HDRIs are plenty for interior IBL (window daylight, reflections).
  Don't pull 8k "just in case" — disk is finite.
- After fetching, recolor/retarget per the canon palette
  (`3d-assets/living-room/SCENE-CANON.md`) — CC0 means we can modify freely.
- Also CC0 and house-relevant: **Kenney** furniture kits (already in
  `docs/research/AI-SCENE-LAYOUT.md` §5), **Quaternius** (owner-approved).
  **KayKit** Furniture Bits is CC0 per the author's own page
  (kaylousberg.com/game-assets/furniture-bits) but downloads via itch.io's
  click flow — needs a browser lane; documented, not fetched.
