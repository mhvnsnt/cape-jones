# The 11 partials — pose sheets, pass files, a test and a recovery save

The middle class of the CN-Leaks-001 survey: files that are neither complete animated scenes nor static libraries. Eight are **GB209 'The Banana' approved pose sheets** — field-guide exports (slate, episode/model boxes, APPROVED stamp) whose root frames are approved poses, several of them built on dedicated gag puppets. Three are production-process files: an **SFX pass** whose base scene does not survive in the archive, a **test export**, and a **recovery save** of a complete scene.

| Partial | Character(s) | Animated frames | Symbols |
|---|---|---|---|
| [gb209-banana-crashed-topshot](gb209-banana-crashed-topshot/) | Gumball, Darwin | 2 root frames (pose sheet); puppet timelines inside run 187 + 149 keyframes | 23 |
| [gb209-banana-bilboquet-sc162](gb209-banana-bilboquet-sc162/) | Gumball, Darwin | 19 poses (pose sheet, rendered & verified in wave 1) | 25 |
| [gb209-banana-gumball-hurt-facekick-sc155](gb209-banana-gumball-hurt-facekick-sc155/) | Gumball | 2 root frames (pose sheet, rendered & verified in wave 1) | 16 |
| [gb209-banana-gumball-hurt-floor-sc160](gb209-banana-gumball-hurt-floor-sc160/) | Gumball | 2f (companion SWF, INDEX-measured) | 15 |
| [gb209-banana-gumball-hurt-himself-sc158](gb209-banana-gumball-hurt-himself-sc158/) | Gumball | 18f of poses (companion SWF, INDEX-measured) | 15 |
| [gb209-banana-darwin-hurt-backkick-sc159](gb209-banana-darwin-hurt-backkick-sc159/) | Darwin | 2f (companion SWF, INDEX-measured) | 11 |
| [gb209-banana-darwin-hurt-himself-sc161](gb209-banana-darwin-hurt-himself-sc161/) | Darwin | 10f of poses (companion SWF, INDEX-measured) | 11 |
| [gb209-banana-destroyed-face-gumball](gb209-banana-destroyed-face-gumball/) | Gumball | 2f (companion SWF, INDEX-measured) | 14 |
| [gb202-remote-sc160-recover](gb202-remote-sc160-recover/) | Gumball, Darwin, Nicole, Richard | Recovery copy of the 31f Sc160 scene (clean file measured at 31f @25) | 69 |
| [gb214-words-sc060-sfx](gb214-words-sc060-sfx/) | Gumball, Darwin (fragments) | 56f of effects (companion SWF, INDEX-measured) | 124 |
| [gb2215-apology-test-export](gb2215-apology-test-export/) | Gumball | Not measured (no companion SWF in the archive) | 26 |

Per-file detail (what exists, what is missing, named cast) is in each folder's `partial.json` and in `../libraries-catalog.json`. Contact sheets are staged in `render_contact_sheets.sh` and blocked by the same write guard as the library model sheets — except the bilboquet poses sheet and the crashed top-shot sheet, which were rendered in wave 1 (statuses are per-record in the catalog).
