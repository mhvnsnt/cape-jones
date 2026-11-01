#!/usr/bin/env python3
"""TOOL 3 — Naming + metadata schema (rank #2).
Toon Boom Harmony / Adobe Animate naming convention, as used in this rig:
  character_part_view_angle_variant
e.g. capejones_arm1_upper_front, capejones_hand3_open_front.
It does NOT detect a shape — it turns a raw proposal into a consistent
canonical label Mars can correct, and flags the known mislabel traps.
Usage: tool3_naming_schema.py <raw_template_name> [source_folder]
"""
import sys, re

# Canonical map from the parts audit (PARTS-LABEL-AUDIT-20261031.md).
# Front/Back in filenames = WHICH LIMB, not body-facing: Arm_Front = ARM1
# (our left), Arm_Back = ARM2 (our right). Same for legs.
CANON = {
    "Arm_Front.png": ("capejones_arm1_upper_lower_front", "ARM 1, our left, whole arm"),
    "Arm_Back.png": ("capejones_arm2_upper_lower_front", "ARM 2, our right, whole arm"),
    "Leg_Front.png": ("capejones_leg1_full_front", "LEG 1, our left, whole leg+foot"),
    "Leg_Back.png": ("capejones_leg2_full_front", "LEG 2, our right, whole leg+foot"),
    "Head_Front.png": ("capejones_head_front", "head, front view, purple cowl+face"),
    "Head_Profile.png": ("capejones_head_profile", "head, side/profile view"),
    "Torso_Chest.png": ("capejones_torso_chest_front", "torso/chest, white suit"),
    "Pelvis.png": ("capejones_pelvis_front", "pelvis/briefs, white"),
    "Belt_Overlay.png": ("capejones_belt_front", "belt overlay, waist"),
    "Cape_Back_Main.png": ("capejones_cape_back_main", "cape, main back drape, black"),
    "Cape_Collar.png": ("capejones_cape_collar_front", "cape collar, neck/shoulders"),
    "Neck.png": ("capejones_neck_front", "neck cylinder, purple"),
    "Hand_1_Fist.png": ("capejones_hand_fist_front", "hand, fist"),
    "Hand_2_FistBack.png": ("capejones_hand_fistback", "hand, fist back"),
    "Hand_3_Open.png": ("capejones_hand_open_front", "hand, open"),
    "Hand_4_Point.png": ("capejones_hand_point_front", "hand, point"),
    "Hand_5_Point2.png": ("capejones_hand_point2_front", "hand, point variant"),
    "Hand_6_Relaxed.png": ("capejones_hand_relaxed_front", "hand, relaxed"),
    "Hand_7_Grip.png": ("capejones_hand_grip_front", "hand, grip"),
    "Eye_White_L.png": ("capejones_eye_white_left", "eye white, left"),
    "Eye_White_R.png": ("capejones_eye_white_right_FLAG", "eye white, right — SHADOW-vs-REJECT exception pending Mars"),
    "Eyes_AngryStrip.png": ("capejones_eyes_angry_strip", "eyes, angry strip"),
    "Face_Angry.png": ("capejones_face_angry_combined_FLAG", "face angry — combined-vs-split exception pending Mars"),
    "Mouth_Closed.png": ("capejones_mouth_closed", "mouth, closed"),
    "Mouth_Open.png": ("capejones_mouth_open", "mouth, open"),
    "Mouth_Shout.png": ("capejones_mouth_shout", "mouth, shout"),
    "Mouth_Smile.png": ("capejones_mouth_smile", "mouth, smile"),
    "Mouth_Teeth.png": ("capejones_mouth_teeth", "mouth, teeth"),
    "Leg_Front_CLEAN.png": ("capejones_leg1_full_front_CLEAN_FLAG", "LEG 1 CLEAN variant — provenance unverified, not canonical"),
    "Leg_Back_CLEAN.png": ("capejones_leg2_full_front_CLEAN_FLAG", "LEG 2 CLEAN variant — provenance unverified, not canonical"),
    "Leg_Back_GRAFTED.png": ("capejones_leg2_full_front_GRAFTED_REJECT", "LEG 2 grafted composite — REJECT as a clean rig piece"),
}

def canonical(raw, source_folder=""):
    warnings = []
    if "CLEAN" in raw:
        warnings.append("CLEAN variant: provenance unverified, not canonical")
    if "GRAFTED" in raw:
        warnings.append("REJECT: grafted composite, do not use as a clean rig piece")
    if raw in ("Arm_Front.png", "Arm_Back.png", "Leg_Front.png", "Leg_Back.png"):
        warnings.append("Front/Back = which limb (left/right), NOT body-facing — do not re-read as facing")
    if source_folder and "fla-back" in source_folder and "front" in raw.lower():
        warnings.append("source folder says back, proposal says front — Mars eye-check required")
    if source_folder and "fla-front" in source_folder and "back" in raw.lower():
        warnings.append("source folder says front, proposal says back — Mars eye-check required")
    if raw not in CANON:
        return {"canonical": "capejones_unknown", "description": "no canonical map entry",
                "warnings": warnings + ["unmapped template — Mars naming required"]}
    name, desc = CANON[raw]
    return {"canonical": name, "description": desc, "warnings": warnings}

if __name__ == "__main__":
    import json
    raw = sys.argv[1]
    folder = sys.argv[2] if len(sys.argv) > 2 else ""
    print(json.dumps({"tool": "naming_schema", "raw": raw, **canonical(raw, folder)}, indent=2))
