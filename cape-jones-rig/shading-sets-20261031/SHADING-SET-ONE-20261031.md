# SHADING SET ONE — BARELY WORKS

Label, exactly as Mars said it (2026-10-31 19:49 CDT): **BARELY WORKS**.
Source: old G2 sheet, limits-broken-10x10-20261031/proofs/G2-shading-10x10-20261031.png,
20 variants, stats copied here as G2-shading-stats-20261031.json. Original untouched.
Base: rig-apose-v7c-clean-transparent.png, 1100x1500, figure bbox x248-875, centre x561.5.
Metric in this set: half-mean left/right R delta only (the old set did not report an edge delta).
Why barely works, in Mars's own words from 2026-10-31 19:23 CDT: all of these look the same
except for the high-contrast one. The old method was a whole-canvas gradient / weak
pseudo-normal tweak, not per-pixel form shading from a real normal field, so the figure
(only 628 px wide in a 1100 px canvas) saw only a small slice of any gradient and the
white suit clipped the bright side.

## Exceptions — visibly moved, NOT true form shading (do NOT upgrade these to definitely works)
- **X08 high contrast — delta -6.1 (L 125.9 / R 132.1).** The one variant Mars said
  visibly differed. It differs because it crushes contrast, not because it shades a form.
  Label: visibly moved / exception, not true form shading.
- **I05 side weight L — delta -18.2 (L 121.6 / R 139.8).** Moved the half-mean the most
  in the old set, by an explicit side weight, not by normal shading.
  Label: visibly moved / exception, not true form shading.
- **I06 side weight R — delta +17.2 (L 138.8 / R 121.5).** Mirror of I05, same caveat.
  Label: visibly moved / exception, not true form shading.
Everything else in this set moved the half-mean by -14.6 to +9.6 and did not read as shading.

## Full table (half-mean R delta)
| Variant | Left R | Right R | Delta R |
|---|---|---|---|
| I01 lambert L | 127.2 | 138.1 | -10.9 |
| I02 lambert R | 137.1 | 127.5 | +9.6 |
| I03 rim only | 133.0 | 133.8 | -0.8 |
| I04 distance norm | 131.6 | 135.6 | -4.0 |
| I05 side weight L | 121.6 | 139.8 | -18.2 |
| I06 side weight R | 138.8 | 121.5 | +17.2 |
| I07 soft normal | 127.2 | 137.2 | -10.0 |
| I08 hard normal | 127.4 | 138.1 | -10.7 |
| I09 top light | 131.1 | 132.0 | -1.0 |
| I10 bottom light | 132.0 | 132.7 | -0.7 |
| X01 pseudo-depth | 124.4 | 138.9 | -14.6 |
| X02 edge-aware | 127.2 | 137.7 | -10.6 |
| X03 faceting test | 119.9 | 121.1 | -1.2 |
| X04 dual light | 132.1 | 132.5 | -0.4 |
| X05 warm/cool split | 127.2 | 138.1 | -10.9 |
| X06 gradient mesh | 130.2 | 135.7 | -5.5 |
| X07 inverted depth | 134.5 | 130.9 | +3.6 |
| X08 high contrast | 125.9 | 132.1 | -6.1 |
| X09 blur relight | 127.2 | 136.8 | -9.5 |
| X10 no shade ctl | 134.7 | 135.5 | -0.8 |

## Verdict
BARELY WORKS, as a set. Keep it only as the record of what did not work, and as the
exception list above. Do not use Set One for production shading. Production shading
is SHADING SET TWO.
Approval: 0/1 for the set labelling + continuation. No repo push. No original overwritten.
