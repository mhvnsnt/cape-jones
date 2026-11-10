# Media checklist — libraries & partials (staged renders)

Every visual below is **staged, not rendered**: at catalog time (2026-11-02) the sandbox write guard refuses binary production-asset writes (PNG frames, MP4) with EPERM / 0-byte results, while text writes pass. The render scripts beside this file (`libraries/render_model_sheets.sh`, `partials/render_contact_sheets.sh`) produce each item the moment the guard lifts. Target for every sheet, once rendered: the item's repo folder AND `~/workspace/your_files/scene-templates/`.

| Item | Kind | Target sheet | Status |
|---|---|---|---|
| gb200-puppet-gumball-v008 | static-puppet-library | sheet-gb200-puppet-gumball-v008.png | blocked-write-guard |
| gb200-puppet-gumball-v006 | static-puppet-library | sheet-gb200-puppet-gumball-v006.png | blocked-write-guard |
| gb200-puppet-gumball-v004 | static-puppet-library | sheet-gb200-puppet-gumball-v004.png | blocked-write-guard |
| gb200-puppet-gumball-v001-cs3 | static-puppet-library | sheet-gb200-puppet-gumball-v001-cs3.png | blocked-write-guard |
| gb200-puppet-darwin-v002 | static-puppet-library | sheet-gb200-puppet-darwin-v002.png | blocked-write-guard |
| gb200-puppet-darwin-v002-dup9 | static-puppet-library | sheet-gb200-puppet-darwin-v002-dup9.png | blocked-write-guard |
| gb200-puppet-darwin-v002-cs5 | static-puppet-library | sheet-gb200-puppet-darwin-v002-cs5.png | blocked-write-guard |
| gb200-puppet-mom-v002 | static-puppet-library | sheet-gb200-puppet-mom-v002.png | blocked-write-guard |
| gb200-puppet-mom-v002-dup10 | static-puppet-library | sheet-gb200-puppet-mom-v002-dup10.png | blocked-write-guard |
| gb200-puppet-dad-v004 | static-puppet-library | sheet-gb200-puppet-dad-v004.png | blocked-write-guard |
| gb200-puppet-dad-v003 | static-puppet-library | sheet-gb200-puppet-dad-v003.png | blocked-write-guard |
| gb200-puppet-anais-v002 | static-puppet-library | sheet-gb200-puppet-anais-v002.png | blocked-write-guard |
| gb200-puppet-anais-v002-dup8 | static-puppet-library | sheet-gb200-puppet-anais-v002-dup8.png | blocked-write-guard |
| gb200-puppet-hector-v001-cs3 | static-puppet-library | sheet-gb200-puppet-hector-v001-cs3.png | blocked-write-guard |
| rig-carrie-ghost | static-puppet-library | sheet-rig-carrie-ghost.png | blocked-write-guard |
| rig-ocho-spider | static-puppet-library | sheet-rig-ocho-spider.png | blocked-write-guard |
| rig-penny-peanutantlers | static-puppet-library | sheet-rig-penny-peanutantlers.png | blocked-write-guard |
| rig-tobias-sportypuff | static-puppet-library | sheet-rig-tobias-sportypuff.png | blocked-write-guard |
| fosters-turn-madam-foster | static-puppet-library | sheet-fosters-turn-madam-foster.png | blocked-write-guard |
| fosters-turn-goo | static-puppet-library | sheet-fosters-turn-goo.png | blocked-write-guard |
| fosters-goo-hair | static-puppet-library | sheet-fosters-goo-hair.png | blocked-write-guard |
| fosters-turn-duchess | static-puppet-library | sheet-fosters-turn-duchess.png | blocked-write-guard |
| fosters-turn-ed | static-puppet-library | sheet-fosters-turn-ed.png | blocked-write-guard |
| fosters-turn-cheese | static-puppet-library | sheet-fosters-turn-cheese.png | blocked-write-guard |
| fosters-turn-frankie | static-puppet-library | sheet-fosters-turn-frankie.png | blocked-write-guard |
| fosters-turn-terrence | static-puppet-library | sheet-fosters-turn-terrence.png | blocked-write-guard |
| fosters-turn-coco | static-puppet-library | sheet-fosters-turn-coco.png | blocked-write-guard |
| fosters-turn-wilt | static-puppet-library | sheet-fosters-turn-wilt.png | blocked-write-guard |
| gb209-banana-crashed-topshot | partial | sheet-gb209-banana-crashed-topshot.png | sheet-delivered-wave1 |
| gb209-banana-bilboquet-sc162 | partial | sheet-gb209-banana-bilboquet-sc162.png | sheet-rendered-wave1-workspace |
| gb209-banana-gumball-hurt-facekick-sc155 | partial | sheet-gb209-banana-gumball-hurt-facekick-sc155.png | blocked-write-guard |
| gb209-banana-gumball-hurt-floor-sc160 | partial | sheet-gb209-banana-gumball-hurt-floor-sc160.png | blocked-write-guard |
| gb209-banana-gumball-hurt-himself-sc158 | partial | sheet-gb209-banana-gumball-hurt-himself-sc158.png | blocked-write-guard |
| gb209-banana-darwin-hurt-backkick-sc159 | partial | sheet-gb209-banana-darwin-hurt-backkick-sc159.png | blocked-write-guard |
| gb209-banana-darwin-hurt-himself-sc161 | partial | sheet-gb209-banana-darwin-hurt-himself-sc161.png | blocked-write-guard |
| gb209-banana-destroyed-face-gumball | partial | sheet-gb209-banana-destroyed-face-gumball.png | blocked-write-guard |
| gb202-remote-sc160-recover | partial | sheet-gb202-remote-sc160-recover.png | blocked-write-guard |
| gb214-words-sc060-sfx | partial | sheet-gb214-words-sc060-sfx.png | blocked-write-guard |
| gb2215-apology-test-export | partial | sheet-gb2215-apology-test-export.png | blocked-write-guard |

Already rendered in wave 1 (workspace copies exist): gb209-banana-bilboquet-sc162 (poses sheet), gb209-banana-crashed-topshot (delivered to your_files).
Source SWFs for the renders: companion SWFs ride inside CN-Leaks-001 next to most FLAs; for binary FLAs without a companion SWF, publish a SWF from the FLA in Adobe Animate first (step 0 in both scripts).
