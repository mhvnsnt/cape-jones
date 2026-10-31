# Cape Jones Pack 4 — Disconnected Heads, Neck Cylinders, Eye Rigs & Mouth Viseme Chart

**Status:** Production specification logged 2026-10-31  
**Purpose:** Modular Drawing Substitution pack for the FLA cutout rig.  
**Style:** 2D hard vector, locked likeness, flat cel-shaded, mid-gray (#808080) background for clean slicing.

## Sheet Generation Prompt (Copy/Paste)

2D animation studio cutout production asset sheet for superhero Cape Jones on a flat neutral mid-gray background (#808080), clean bold black vector ink outlines, flat cel-shaded cartoon style. Row 1: 5 disconnected blank head bases with smooth purple cowl and exposed tan muscular jawline (no mouth drawn on the jaw) showing turnaround angles (Front, 3/4 Front, Side Profile, 3/4 Back, Full Back) plus 1 extreme furious scowl head with deep brow wrinkles. Row 2: 5 disconnected purple muscular neck cylinders with grey ball-joint pivot caps at top and bottom across matching angles. Row 3: 8 isolated purple-and-black mask eye strips with white angular superhero eyes (neutral glare, furious furrowed brow, wide shock, half-lidded deadpan bored, narrow squint, closed blink, side glance, one-brow raised). Rows 4 and 5: 14 isolated lip-sync mouth visemes on small tan chin patches for both Front and 3/4 angles (closed neutral, brooding frown, A/I wide open, E stretched teeth, O round, U tight pucker, F/V teeth on lip, L/N tongue up, Th tongue between teeth, S/Z clenched gritted teeth, extreme snarl, roar, deadpan slack mouth, cocky smirk). Evenly spaced islands for easy slicing.

## What Goes Inside Pack 4 (Row-by-Row)

- **Row 1 — 5 Blank Head Bases + High-Detail Expression Swap:** Five completely mouthless head bases (purple cowl + angular mask eye bridge + smooth tan jaw) across Front (0°), 3/4 Front (45°), Side Profile (90°), 3/4 Back (135°), and Full Back (180°), plus a dedicated Extreme Scowl Head.
- **Row 2 — 5 Disconnected Purple Neck Cylinders:** Detached neck columns with rounded gray ball-joint caps on both ends. Includes Front, 3/4, Side, Back, and a Strained Tendon Neck.
- **Row 3 — 8 Mask Eye & Brow Strips:** Neutral Glare, Furious Furrowed Scowl, Wide Alert, Half-Lidded Deadpan, Tight Squint, Closed Blink, Side Glance, Skeptical One-Brow Raise.
- **Rows 4 & 5 — 14-Shape Lip-Sync Viseme Chart (Front & 3/4 Sets):** Isolated mouths on tan chin patches.

## How to Pack & Rig Sheet 4 in the .FLA

Build a Nested Head_Master Graphic Symbol with 4 internal layers (top to bottom):
1. Facial_Creases_Overlay (optional)
2. Eyes_Mask_Swap (8 eye states on Frames 1–8)
3. Mouth_Visemes (14 front mouths on 1–14, 3/4 on 15–28, profile on 29–36)
4. Head_Base_Turnaround (5 blank angles on Frames 1–5)

Lock registration so the base of the skull sits on the symbol's (0,0) center. Flip Horizontal for right-side angles. Optional Animate Lip-Syncing Settings for phoneme mapping.

## Modular Pack System (Full Rig)

Real broadcast studios split the rig into 5 high-resolution modular Drawing Substitution packs:

- **Pack 1:** Disconnected Arms, Gauntlets & Hands Master Sheet
- **Pack 2:** Disconnected Legs (Thighs, V-Trim Shins & Boots/Feet Across Angles)
- **Pack 3:** Torso, Chest Emblem, Utility Belt & Pelvis Turnaround/Tilt Pack
- **Pack 4:** Head Angles, Neck Cylinders, Eye Rigs & Mouth Viseme Chart (this document)
- **Pack 5:** Multi-State Cape Pack (Collar Drapes, Idle Hang, Billowing Action, Seated Throne Drape)

## Master Layer Hierarchy (Top to Bottom)

Hand_Front → Forearm_Front → UpperArm_Front → Cape_Collar → Eyes_Swap → Mouth_Visemes → Head_Base → Neck → Belt_Overlay → Torso_Chest → Pelvis → Foot_Front → Shin_Front → Thigh_Front → Foot_Back → Shin_Back → Thigh_Back → Hand_Back → Forearm_Back → UpperArm_Back → Cape_Back_Main

## Joint Rules

Every upper arm, forearm, thigh, and shin needs a rounded circular ball-joint cap on the hidden end. Pivot at the center of the circle cap. Parenting: Hand → Forearm → UpperArm → Torso; Foot → Shin → Thigh → Pelvis; Head → Neck → Torso.

## Current Locked References

See `../variations/references/` for the locked T-pose front views that define the proportions and likeness for all packs.
