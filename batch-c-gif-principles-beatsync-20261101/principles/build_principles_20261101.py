"""Per-shot 12-principles check, CJ-01..CJ-30, 2026-11-01.
Basis: shots-final-painted-bg-20261101.json (measured) + V6 spec holds + finals REPORT.
Verdicts: P=PASS, PA=PARTIAL, F=FAIL, NA=N/A (single still cannot show it).
FAIL = evidence in this still CONTRADICTS the principle. A stand-in, a demo-only
grade, a post-episode item, or a motion-only item is PA or NA, never upgraded to
P and never hidden as F. No shot approval is claimed: approval stays 0/30."""
import json, csv, os
BASE='/home/hatch/workspace/cape-jones-rig/shots-final-painted-bg-20261101'
OUT=os.path.dirname(os.path.abspath(__file__))
shots=json.load(open(f'{BASE}/shots-final-painted-bg-20261101.json'))
PR=['Squash & stretch','Anticipation','Staging','Straight-ahead / pose-to-pose',
    'Follow-through & overlap','Slow in & slow out','Arcs','Secondary action',
    'Timing','Exaggeration','Solid drawing','Appeal']
P,PA,F,NA='P','PA','F','NA'
def fill(default, over):
    d={s['shot_id']:default for s in shots}
    d.update(over); return d
V={}
V[0]=fill(PA,{'CJ-02':P,'CJ-03':P,'CJ-13':P,'CJ-14':P,'CJ-18':P,'CJ-19':P})
V[1]=fill(NA,{'CJ-01':P,'CJ-16':P,'CJ-02':PA,'CJ-03':PA,'CJ-04':PA,'CJ-05':PA,
  'CJ-09':PA,'CJ-10':PA,'CJ-11':PA,'CJ-12':PA,'CJ-13':PA,'CJ-14':PA,'CJ-15':PA,
  'CJ-17':PA,'CJ-18':PA,'CJ-19':PA,'CJ-20':PA,'CJ-21':PA,'CJ-22':PA,'CJ-27':PA})
V[2]=fill(P,{'CJ-05':PA,'CJ-29':PA})
V[3]=fill(P,{})
V[4]=fill(NA,{'CJ-04':P,'CJ-02':PA,'CJ-03':PA,'CJ-13':PA,'CJ-14':PA,'CJ-22':PA})
V[5]=fill(NA,{})
V[6]=fill(PA,{'CJ-01':P,'CJ-02':P,'CJ-13':P,'CJ-14':P,
  'CJ-23':NA,'CJ-24':NA,'CJ-25':NA,'CJ-26':NA,'CJ-27':NA,'CJ-28':NA,'CJ-29':NA,'CJ-30':NA})
V[7]=fill(PA,{'CJ-04':P,'CJ-06':P,'CJ-07':P,'CJ-08':P,'CJ-09':P,'CJ-10':P,'CJ-11':P,
  'CJ-21':P,'CJ-22':P,'CJ-23':P,'CJ-24':P,'CJ-28':P,'CJ-29':P})
V[8]=fill(NA,{'CJ-01':PA,'CJ-02':PA,'CJ-03':PA,'CJ-04':PA,'CJ-05':PA,'CJ-06':PA,
  'CJ-07':PA,'CJ-08':PA,'CJ-09':PA,'CJ-10':PA,'CJ-11':PA,'CJ-12':PA,'CJ-13':PA,
  'CJ-14':PA,'CJ-15':PA,'CJ-16':PA,'CJ-17':PA,'CJ-18':PA,'CJ-19':PA,'CJ-20':PA,
  'CJ-21':PA,'CJ-22':PA})
V[9]=fill(PA,{'CJ-02':P,'CJ-03':P,'CJ-11':P,'CJ-13':P,'CJ-14':P,'CJ-18':P,'CJ-19':P,'CJ-27':P})
V[10]=fill(P,{'CJ-15':PA,'CJ-18':PA,'CJ-22':PA})
V[11]=fill(P,{'CJ-01':PA,'CJ-02':PA,'CJ-05':PA,'CJ-15':PA,'CJ-23':PA,'CJ-25':PA,
  'CJ-26':PA,'CJ-27':PA,'CJ-29':PA})
# basis phrases per principle per shot-group, with measured numbers injected later
BASIS={
0:{'P':'pose shows it + measured width/effect (see row numbers)',
   'PA':'no squash/stretch frame in this single still, or volume constancy not measurable from one still'},
1:{'P':'this frame IS the anticipation (V6 spec hold, windup / before-tighten)',
   'PA':'anticipation lives in the series (prior shot / movement frame), not in this frame',
   'NA':'cyclic hold / seated / standing still: no big move to anticipate in this shot'},
2:{'P':'one idea, hero centred, margins symmetric, clipped=False',
   'PA':'staging weakened by an unresolved call / stand-in BG (see shot note)'},
3:{'P':'pose-to-pose method: joint-locked key pose first (checklist); builder-exact figure',
   'PA':'','NA':''},
4:{'P':'follow-through residue visible in this still (afterglow) after the main action',
   'PA':'follow-through element present (burst/lines/streaks) but lag vs body not measurable from one still',
   'NA':'cape/secondary lag needs consecutive frames; not observable in this single still'},
5:{'NA':'easing/spacing needs consecutive frames; V6 spec hold is an endpoint, not easing — motion check owed'},
6:{'P':'effect lines trace the limb path in this still',
   'PA':'path implied by pose/effect, no drawn trajectory to measure in this still',
   'NA':'static seated/standing still: no limb path to check'},
7:{'P':'secondary element present and subordinate (measured effect px, subordinate to hero)',
   'PA':'effect present but it is the main effect, or a proxy (device-glow, beat-halo) — not a separate subordinate action'},
8:{'PA':'timing written in V6 spec (holds in frames) but duration cannot be verified from a single still — motion check owed',
   'NA':'no timing spec in V6 for this still (dialogue/seated/standing post-episode or hold)'},
9:{'P':'pose pushed past realism and still joint-locked (width / burst / L3 shafts measured)',
   'PA':'reference / neutral / recover pose: exaggeration not demanded in this frame'},
10:{'P':'clipped=False, feet=ground (or documented airborne offset), consistent char height, joint-locked plate',
    'PA':'stand-in plate / seam candidate / V6 tuck blocker: volume not yet final in this still'},
11:{'P':'no debug labels in final, rim present (rim px measured), character reads as Cape Jones',
    'PA':'demo-only grade / stand-in BG / non-canonical room / post-episode dialogue: look not final'},
}
rows=[]
for s in shots:
    sid=s['shot_id']
    verdicts=[V[i][sid] for i in range(12)]
    rows.append((s,verdicts))
    assert len(verdicts)==12
# counts
lines=[]
lines.append('# Per-shot 12-principles checks — CJ-01 to CJ-30 — 2026-11-01 (Batch C)')
lines.append('')
lines.append('**Approval: 0/30 — this check does NOT approve any shot. It is a measurement pass only.**')
lines.append('**Sources (measured, not generic):** `shots-final-painted-bg-20261101/shots-final-painted-bg-20261101.json` + `REPORT-20261101.md` + `SHOT-SPECS-V6-20261031.md` + `12-PRINCIPLES-CHECKLIST-20261031.md`.')
lines.append('Every still below was checked against its own JSON numbers (canvas, char W×H, bbox, feet vs ground, clipped, rim px, bleed px, effect + effect px, shafts, dual-light) and its own shot note. A single still cannot show motion: those cells are N/A, not PASS.')
lines.append('')
lines.append('## Verdict key')
lines.append('- **P (PASS):** evidence in this still + spec supports the principle.')
lines.append('- **PA (PARTIAL):** partly present, or present only at series level / as a stand-in / demo-only grade / proxy — the gap is named per shot, not hidden.')
lines.append('- **F (FAIL):** evidence in this still contradicts the principle.')
lines.append('- **NA (N/A):** this single still + spec cannot show it (motion-only, or no such move in the shot). Excluded from the assessable denominator.')
lines.append('')
lines.append('## Counts per principle (30 shots each)')
lines.append('')
lines.append('| # | Principle | PASS | PARTIAL | FAIL | N/A | Assessable (P+PA+F) | PASS % of assessable | PASS % of 30 | Shots PARTIAL | Shots FAIL |')
lines.append('|---|---|---|---|---|---|---|---|---|---|---|')
for i,name in enumerate(PR):
    vs=[V[i][s['shot_id']] for s in shots]
    p,pa,f,na=[vs.count(x) for x in (P,PA,F,NA)]
    ass=p+pa+f
    ppa=f'{100*p/ass:.1f}%' if ass else 'n/a (0 assessable)'
    pp30=f'{100*p/30:.1f}%'
    pa_shots=', '.join(s['shot_id'] for s in shots if V[i][s['shot_id']]==PA) or '—'
    f_shots=', '.join(s['shot_id'] for s in shots if V[i][s['shot_id']]==F) or '— (none)'
    lines.append(f'| {i+1} | {name} | {p} | {pa} | {f} | {na} | {ass} | {ppa} | {pp30} | {pa_shots} | {f_shots} |')
tot_p=sum(V[i][s['shot_id']]==P for i in range(12) for s in shots)
tot_pa=sum(V[i][s['shot_id']]==PA for i in range(12) for s in shots)
tot_f=sum(V[i][s['shot_id']]==F for i in range(12) for s in shots)
tot_na=sum(V[i][s['shot_id']]==NA for i in range(12) for s in shots)
lines.append('')
lines.append(f'**Totals, 360 cells (30 shots × 12 principles): PASS {tot_p} ({100*tot_p/360:.1f}% of all cells), PARTIAL {tot_pa} ({100*tot_pa/360:.1f}%), FAIL {tot_f} ({100*tot_f/360:.1f}%), N/A {tot_na} ({100*tot_na/360:.1f}%). PASS of assessable cells ({tot_p+tot_pa+tot_f} cells): {100*tot_p/(tot_p+tot_pa+tot_f):.1f}%.**')
lines.append('')
lines.append('**FAIL = 0/360 is a narrow claim, stated plainly:** no still contradicts a principle. It is NOT a claim that the work is finished: 140 cells are PARTIAL (stand-ins, demo-only grades, series-level-only evidence, proxies, post-episode items) and 80 cells are N/A (motion checks still owed — above all slow-in/out 30/30 N/A and timing 0 PASS, because a single still cannot verify easing or duration). The motion pass (consecutive frames) is the owed follow-up that can move N/A/PA cells, not a re-grade of these stills.')
lines.append('')
lines.append('## Verdict matrix (P / PA / F / NA)')
lines.append('')
lines.append('| Shot | 1 S&S | 2 Antic | 3 Stag | 4 P2P | 5 Follow | 6 Slow | 7 Arcs | 8 Second | 9 Timing | 10 Exagg | 11 Solid | 12 Appeal | PASS count |')
lines.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for s,vs in rows:
    pc=vs.count(P)
    lines.append(f"| {s['shot_id']} {s['slug']} | {' | '.join(vs)} | {pc}/12 |")
lines.append('')
lines.append('## Per-shot detail — measured numbers + basis per principle')
lines.append('')
lines.append('Measured shorthand per row: canvas; char W×H; feet−ground (0 = grounded, negative = airborne above ground line); clipped; effect + effect px; rim px; shafts; dual-light where present. V6 holds cited where the spec gives them.')
lines.append('')
SPEC_HOLD={'CJ-01':'windup hold 6','CJ-02':'extend-snap hold 2','CJ-03':'impact hold 12','CJ-04':'recover hold 6',
 'CJ-06':'walk contact hold 12','CJ-07':'walk passing hold 12','CJ-08':'walk hold 12',
 'CJ-09':'dance hold 12','CJ-10':'dance hold 12','CJ-11':'dance finale hold 12',
 'CJ-12':'flying hold 12','CJ-13':'flying hold 12','CJ-14':'flying hold 12','CJ-15':'flying hold 12',
 'CJ-16':'flex apose hold 6 before flex hold 24','CJ-17':'arms-up reference','CJ-18':'flex hold 24','CJ-19':'fighting pose','CJ-20':'arms-up high',
 'CJ-21':'jump crouch 6 / takeoff 2','CJ-22':'jump tuck 12 / land 6'}
SHOT_NOTE={
 'CJ-01':'windup frame; JOJO-TENSION demo-only grade.',
 'CJ-02':'extend-snap frame; JOJO-TENSION demo-only grade; widest punch char (722 px).',
 'CJ-03':'impact-locked frame; pink leader streak from old final absent in this new figure (builder-exact).',
 'CJ-04':'recover frame; tension/power beats closed here.',
 'CJ-05':'across-down PLACEMENT frame, NOT impact; town BG per spec, street-vs-town call still open.',
 'CJ-15':'PLATE STAND-IN: hover plate; true foreshortened forearm piece still owed; grade/BG/effects are final-pattern.',
 'CJ-17':'arms-up REFERENCE pose, NOT a flex; same plate as CJ-20, different spec.',
 'CJ-18':'base double-bicep plate; FAILED fists-in file NOT used; pose-space seam candidate exists separately.',
 'CJ-20':'same arms-up plate as CJ-17, different spec (grade/BG/effect differ).',
 'CJ-21':'hero = takeoff frame (airborne); crouch frame is movement frame A of the same shot, not this still.',
 'CJ-22':'hero = landing frame (grounded); tuck frame is airborne (110 px above ground) in the same shot movement.',
 'CJ-23':'sage-lounge room painting, NOT canonical purple/pink neon room (room flag, canonical repaint owed).',
 'CJ-25':'sage-lounge room; device-glow is a prop-glow proxy, device prop sheet is a separate asset.',
 'CJ-26':'JOJO-UNCERTAINTY demo-only, near-B&W; dialogue/visemes POST-EPISODE, not a hold.',
 'CJ-27':'red-alert LUT key; dialogue POST-EPISODE.',
 'CJ-29':'night-city painting owed; rooftop-painted graded night used as stand-in.',
 'CJ-30':'dual-light: front magenta-rose + back cyan, both sources named in spec.',
 'CJ-19':'dual-light: front warm amber + back cyan, both sources named in spec.',
}
for s,vs in rows:
    sid=s['shot_id']; cw,ch=s['char_size']; air=s['feet_y']-s['ground_y']
    lines.append(f"### {sid} — {s['slug']}")
    lines.append(f"Measured: canvas {s['canvas'][0]}×{s['canvas'][1]}; char {cw}×{ch}; feet−ground {air} px; clipped={s['clipped']}; effect {s['effect']} {s['effect_px']} px; rim {s['rim']} {s['rim_px']} px; shafts {s['shaft_count']}; dual={s['dual_light']}; spec: {SPEC_HOLD.get(sid,'no V6 timing spec (hold/post-episode)')}. {SHOT_NOTE.get(sid,'')}")
    for i,name in enumerate(PR):
        v=vs[i]; b=BASIS[i].get(v,'')
        lines.append(f"- {i+1}. {name}: **{v}** — {b}")
    lines.append('')
lines.append('## What this check does NOT do (plainly)')
lines.append('- It does not approve any shot: approval stays 0/30, Mars look still owed for all 30.')
lines.append('- It does not verify motion: slow-in/out (0/30 assessable), timing (0/30 PASS), follow-through lag (24/30 N/A) and arcs-as-paths need consecutive frames, not stills. That motion pass is owed, not claimed.')
lines.append('- It does not resolve the open calls it names: CJ-05 street-vs-town, CJ-23/25/27 canonical room repaint, CJ-15 foreshortened piece, CJ-18 seam candidate, CJ-26 rim QC, CJ-29 night-city painting, dialogue/visemes post-episode.')
lines.append('- It does not re-claim the finals gates: builder-exact / pixel-identical gates from REPORT-20261101.md are cited as the solid-drawing / pose-to-pose basis, not re-run here.')
with open(os.path.join(OUT,'12-principles-per-shot-20261101.md'),'w') as f:
    f.write('\n'.join(lines))
with open(os.path.join(OUT,'12-principles-matrix-20261101.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['shot','slug']+PR+['pass_count'])
    for s,vs in rows:
        w.writerow([s['shot_id'],s['slug']]+vs+[vs.count(P)])
print(f'TOTALS P={tot_p} PA={tot_pa} F={tot_f} NA={tot_na} cells=360')
for i,name in enumerate(PR):
    vs=[V[i][s['shot_id']] for s in shots]
    print(f"{i+1:2d} {name}: P={vs.count(P)} PA={vs.count(PA)} F={vs.count(F)} NA={vs.count(NA)}")
print('per-shot PASS counts:', {s['shot_id']:vs.count(P) for s,vs in rows})
