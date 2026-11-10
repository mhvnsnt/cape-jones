# Path Patch Notes — RESEARCH-INDEX.md

Apply these replacements in `docs/research/RESEARCH-INDEX.md`:

1. SOUNDTRACKS row:
   - Old: `MP3s in cape-jones-build/`
   - New: `MP3s in production/assets/soundtracks/` (or actual location once confirmed)

2. docs/cloud/OPENCODE.md row:
   - Old: `opencode/ source in production/devtools/`
   - New: `opencode/ source in production/devtools/` — verify the folder exists; if not, mark as external or remove the claim.

3. EXPANSION-4 row:
   - Already correct on the “resolved” part; add note that InstanceAnimator and LDF-VFI now live in `production/tools/` and have wrappers in `production/pipeline/`.

After editing, the stale `~/workspace/tools/` references in EXPANSION-4.md are clarified in the patched copy under `docs/research/EXPANSION-4.md` in this fixes folder.
