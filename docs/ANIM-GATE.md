# Animation gate — fight vs show (mirror of western-heart, owner t117u)

Canonical implementation lives in western-heart: `game/js/anim-gate.js`, allowlist `game/data/crossover.json`,
CI test `test/anim-gate.test.mjs` (PR mhvnsnt/western-heart#811).

Rules that apply to anything Cape Jones (show) hands to the game:
- Contexts: FIGHT, INTRO_OUTRO, CUTSCENE (story), SHOW.
- In FIGHT only moveset clips play. Any show clip (`anims/show/*`, `show:*`, or tagged `userData.animSet='show'`) is rejected and logged `[WH-ANIM-GATE]`.
- Crossover only through `crossover.json`: fight clips may go to SHOW / CUTSCENE / INTRO_OUTRO; show clips may go to INTRO_OUTRO / CUTSCENE / SHOW, never FIGHT, unless the owner approves it in a moveset PR.
- Show clips authored here must be exported under `anims/show/` names so the gate can recognise them.
