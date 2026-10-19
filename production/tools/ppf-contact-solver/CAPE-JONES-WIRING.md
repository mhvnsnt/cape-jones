# ZOZO ppf-contact-solver — Cape Jones Wiring

**What:** ZOZO's open-source cloth / soft-body / rope physics solver — the
best open cloth simulation available in 2026. Finite Element (FEM) solver with
a polynomial barrier contact model that **guarantees no mesh intersection**
and strict strain limits (triangles never stretch beyond a user-set %, e.g.
1–5%). Published at SIGGRAPH Asia 2024 (ACM Transactions on Graphics).
Handles 180M+ contact points on a single GPU.

**Source:** https://github.com/st-tech/ppf-contact-solver
**License:** Apache-2.0 — verified from vendored `LICENSE`. Commercial use
allowed: use, modify, redistribute in proprietary products royalty-free;
preserve the license notice and attribution.
**Vendored:** `blender_addon/` (v1.0.16), `LICENSE`, `README.md`,
`CITATION.cff` — pulled 2026-10-18 from `st-tech/ppf-contact-solver` main.
**Status: UPGRADE PATH** — the Blender add-on requires **Blender 5.0+**
(`blender_version_min = "5.0.0"` in `blender_manifest.toml`). Our pipeline
runs Blender 4.0.2, so the add-on does not install here yet. Vendored now so
the code is in-repo the day the pipeline upgrades; the solver core is also
usable standalone (see below).

## Why this fills the gap

Our current cloth/secondary stack is Wiggle 2 (spring physics on bone chains —
great for the cape's *secondary motion*) plus Blender's built-in cloth sim.
What neither gives us is **guaranteed non-penetrating, strain-limited cloth**:
the cape clipping through the body/shoulders on fast moves is exactly the
failure class this solver eliminates by construction. Houdini Vellum and
Marvelous Designer are the commercial references ($100s–$1000s/seat/yr);
this is the Apache-2.0 answer.

## Architecture (matters for wiring)

```
blender_addon/  → Blender 5.0+ extension (UI, scene export, result import)
       │  TCP + CBOR
       ▼
ppf-cts-server  → Rust solver binary (local or remote/cloud GPU)
```

The solver is a **separate server process**. The Blender add-on ships scene
geometry + material params to it and fetches animation frames back. This means:

1. The solver can run on a **remote/cloud GPU** (vast.ai L4 ≈ $0.50/hr;
   a drape sim ≈ $0.10) while Blender runs locally — macOS-laptop-friendly.
2. Every tool is exposed over an **MCP server** — an LLM agent can build and
   launch a sim from a sentence.
3. The solver is **not real-time** — built for offline rendering correctness,
   not playback speed. Fits our bake-to-keyframes pipeline perfectly.

## Wiring for the Cape Jones cape (once on Blender 5.0+)

1. **Get the solver:** either build from `crates/` (Rust toolchain), or grab a
   prebuilt `ppf-cts-server` + add-on zip from the upstream GitHub Releases
   (they publish dated builds, e.g. `addon-2026-10-19-0917`).
2. **Install the add-on** from the vendored `blender_addon/` directory
   (Blender 5.0+: *Edit → Preferences → Extensions → Install from Disk*).
3. **Cape setup:** select the cape mesh → add to a solver ObjectGroup →
   material preset `Silk`/`Cotton` (see `example_material_profile.toml`) →
   pin the shoulder attachment verts (pin group at the cape's neck/shoulder
   seam) → add the body mesh as a collider.
4. **Run:** Transfer → solver runs (local or remote) → fetch frames back as
   a baked mesh cache → convert to shape keys or bind to the cape bone chain.
5. **Combine with Wiggle 2:** use the solver for the *hero drape/cloth*
   (guaranteed no-clip), Wiggle 2 for *procedural secondary jiggle* on top.
   They solve different problems; the stack is solver → bake → wiggle.

## Cape Jones specifics

- Scale lock: 0.925 m character. Set the solver's scene units to meters and
  verify the cape's rest drape matches the current 48-baked-shape-key look
  before accepting a sim.
- The cape is currently fused-shape-key animation; the solver path replaces
  hand-keyed drape with physics, baked to keyframes — same delivery format,
  no pipeline change downstream.

## Honest caveats (from the author's own notes + 80.lv)

- "It's slow, the UI still involves many manual steps, and there are still
  rough edges." Offline-quality, not interactive.
- Community add-ons also exist: **AndoSim**, **ArzteZ-PPF-solver**.
- Not a drop-in Marvelous Designer replacement; pattern/sewing UX is thinner.

## License & provenance

- `LICENSE` — Apache License 2.0 (vendored, own-eyes verified 2026-10-18).
- Upstream: https://github.com/st-tech/ppf-contact-solver · ZOZO, Inc.
- Citation: see `CITATION.cff`.
- Commercial use: allowed royalty-free; keep the license notice + attribution.
