# The 28 static puppet libraries — FLA character-sheet libraries

Owner's correction, logged (2026-11-02): what the wave-1 survey called "static — not a scene" is what a studio calls a **static puppet library** — the FLA character-sheet library a character is built from: heads, face comps, mouth and eye sets, bodies, pose sets, props. These are the 28 libraries inside `CN-Leaks-001-gumball.zip`, censused one by one. Every character is named from the file data; every part count comes from the file's own symbol list (XFL scan) or, for the pre-XFL binary FLAs, from names recovered out of the file's strings in-memory (the file itself was never modified).

Three families:

- **GB200 original puppet block (14)** — the show's own master libraries: Gumball (x4 saves), Darwin (x3), Nicole/Mom (x2), Richard/Dad (x2), Anais (x2), Hector (x1). The XFL-readable saves are complete three-view puppet systems (front / back / flopped) that assemble as-is. The two CS3 saves are binary; their documented shape sets (eye shapes / big-cheek mouths / lipsynch / eating heads) were recovered by name.
- **Gumball S2 loose rigs (4)** — Carrie (ghost), Ocho (spider form), Penny (peanut-with-antlers form), Tobias (sporty puff): small single-character form rigs, all binary; Penny's is the only one whose complete part list survives by name.
- **Foster's model turns (10)** — a second show's library family riding inside the same archive's FOSTERS folder: model-turn FLAs for Madame Foster, Goo, Duchess, Ed, Cheese, Frankie, Terrence, Coco, Wilt, plus Goo's hair as a single-element file. These are working character files (Frankie's is an 18 MB part-by-part system referencing a whole parts folder), all binary OLE2, censused from recovered names and the files' own internal references.

Media status: model-sheet renders for all 28 are staged (`render_model_sheets.sh` in this folder's parent) but **blocked at catalog time by the sandbox write guard**, which refuses rendered-binary writes (EPERM / 0 bytes) while text writes pass. The per-item checklist is in `../MEDIA-CHECKLIST.md`; each record's `media.status` says the same thing plainly. The moment the guard lifts, sheets land next to each record and in `~/workspace/your_files/scene-templates/`.

| Library | Character(s) | Symbols | Completeness |
|---|---|---|---|
| [gb200-puppet-gumball-v008](gb200-puppet-gumball-v008/) | Gumball | 61 | Complete — assembles in full |
| [gb200-puppet-gumball-v006](gb200-puppet-gumball-v006/) | Gumball | 61 | Complete — assembles in full (earlier save) |
| [gb200-puppet-gumball-v004](gb200-puppet-gumball-v004/) | Gumball | 61 | Complete — assembles in full (earlier save) |
| [gb200-puppet-gumball-v001-cs3](gb200-puppet-gumball-v001-cs3/) | Gumball | binary — see record | Presumed complete (version-001 original) — census is strings-level only |
| [gb200-puppet-darwin-v002](gb200-puppet-darwin-v002/) | Darwin | 34 | Complete — assembles in full |
| [gb200-puppet-darwin-v002-dup9](gb200-puppet-darwin-v002-dup9/) | Darwin | binary — see record | Complete — assembles in full (duplicate copy) |
| [gb200-puppet-darwin-v002-cs5](gb200-puppet-darwin-v002-cs5/) | Darwin | 34 | Complete — assembles in full (CS5 save) |
| [gb200-puppet-mom-v002](gb200-puppet-mom-v002/) | Nicole (Mom) | 38 | Complete — assembles in full |
| [gb200-puppet-mom-v002-dup10](gb200-puppet-mom-v002-dup10/) | Nicole (Mom) | binary — see record | Complete — assembles in full (duplicate copy) |
| [gb200-puppet-dad-v004](gb200-puppet-dad-v004/) | Richard (Dad) | 46 | Complete — assembles in full (richest Dad save) |
| [gb200-puppet-dad-v003](gb200-puppet-dad-v003/) | Richard (Dad) | 43 | Complete — assembles in full (earlier save) |
| [gb200-puppet-anais-v002](gb200-puppet-anais-v002/) | Anais | 48 | Complete — assembles in full |
| [gb200-puppet-anais-v002-dup8](gb200-puppet-anais-v002-dup8/) | Anais | binary — see record | Complete — assembles in full (duplicate copy) |
| [gb200-puppet-hector-v001-cs3](gb200-puppet-hector-v001-cs3/) | Hector | binary — see record | Documented shape-set library — full census needs the file opened in Flash/Animate |
| [rig-carrie-ghost](rig-carrie-ghost/) | Carrie | binary — see record | Rig present; part census partial — most symbol names not string-recoverable |
| [rig-ocho-spider](rig-ocho-spider/) | Ocho | binary — see record | Minimal rig — named parts only; completeness limited |
| [rig-penny-peanutantlers](rig-penny-peanutantlers/) | Penny | binary — see record | Complete minimal puppet — every part named and present |
| [rig-tobias-sportypuff](rig-tobias-sportypuff/) | Tobias | binary — see record | Head/face rig by name — body parts not name-recovered |
| [fosters-turn-madam-foster](fosters-turn-madam-foster/) | Madame Foster | binary — see record | Model-turn library — large symbol count behind generic names |
| [fosters-turn-goo](fosters-turn-goo/) | Goo | binary — see record | Model-turn library with special-pose extensions |
| [fosters-goo-hair](fosters-goo-hair/) | Goo (hair only) | binary — see record | Single-element sheet — hair comps only, NOT a character |
| [fosters-turn-duchess](fosters-turn-duchess/) | Duchess | binary — see record | Model-turn library with separately-kept hand/eyelash pieces |
| [fosters-turn-ed](fosters-turn-ed/) | Ed (Eduardo) | binary — see record | Model-turn library with performance comps (head turn/talk, mouth shapes, hair cycle) |
| [fosters-turn-cheese](fosters-turn-cheese/) | Cheese | binary — see record | Model-turn library with alternate heads/mouths and a numbered hand library |
| [fosters-turn-frankie](fosters-turn-frankie/) | Frankie | binary — see record | Full part-by-part character system (3/4-view set) — the deepest Foster's library in the archive |
| [fosters-turn-terrence](fosters-turn-terrence/) | Terrence | binary — see record | Model-turn library with dedicated mouth-shape sets |
| [fosters-turn-coco](fosters-turn-coco/) | Coco | binary — see record | Model-turn library with walk/run leg pieces and head comps |
| [fosters-turn-wilt](fosters-turn-wilt/) | Wilt | binary — see record | Model-turn library with a four-view set (front / 3-4 front / side / back) |

Machine-readable records: `../libraries-catalog.json` (all 39 libraries + partials, same schema family as the scenes CATALOG) and one `library.json` per folder here.
