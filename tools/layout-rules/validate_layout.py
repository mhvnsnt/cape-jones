#!/usr/bin/env python3
"""Headless validator for furniture layouts.

Checks a layout JSON (see living_room_layout.json example format below) against
the interior-design rule corpus in layout_rules.json. Runs with NO Blender and
NO GPU, so the build lane can iterate in seconds.

Usage:
    python validate_layout.py <layout.json> [--rules layout_rules.json]

layout.json format:
{
  "room": {"width_m": 5.0, "depth_m": 4.0},
  "items": [
    {"name": "loveseat", "w": 1.6, "d": 0.8, "x": 2.5, "z": 1.2,
     "rot_deg": 0, "facing": [0, -1], "kind": "seat"},
    {"name": "tv_stand", "w": 1.2, "d": 0.5, "x": 2.5, "z": 3.6,
     "rot_deg": 180, "kind": "tv", "screen_diagonal_m": 0.8}
  ],
  "walkway_from": "doorway", "doorway": {"x": 0.9, "z": 0.0, "width_m": 0.9}
}

Exits 0 when all checks pass, 1 with a violation report otherwise.
"""

import json
import math
import sys

ROTD = math.pi / 180.0


def rotated_half_extents(w, d, rot_deg):
    r = rot_deg * ROTD
    c, s = abs(math.cos(r)), abs(math.sin(r))
    return (w * c + d * s) / 2.0, (w * s + d * c) / 2.0


def aabb(item):
    hx, hz = rotated_half_extents(item["w"], item["d"], item.get("rot_deg", 0))
    return (item["x"] - hx, item["x"] + hx, item["z"] - hz, item["z"] + hz)


def overlap(a, b):
    ix = min(a[1], b[1]) - max(a[0], b[0])
    iz = min(a[3], b[3]) - max(a[2], b[2])
    return max(0.0, ix) * max(0.0, iz)


def edge_gap(a, b):
    ix = min(a[1], b[1]) - max(a[0], b[0])
    iz = min(a[3], b[3]) - max(a[2], b[2])
    if ix >= 0 and iz >= 0:
        return 0.0  # overlapping
    return max(-ix if ix < 0 else 0.0, -iz if iz < 0 else 0.0)


def center(a):
    return ((a[0] + a[1]) / 2.0, (a[2] + a[3]) / 2.0)


def main():
    layout_path = sys.argv[1]
    rules_path = sys.argv[2] if len(sys.argv) > 2 else "layout_rules.json"
    layout = json.load(open(layout_path))
    rules = json.load(open(rules_path))
    room = layout["room"]
    W, D = room["width_m"], room["depth_m"]
    items = layout["items"]
    boxes = {it["name"]: aabb(it) for it in items}
    by_kind = {}
    for it in items:
        by_kind.setdefault(it.get("kind", "prop"), []).append(it)
    violations = []

    # 1. inside room bounds
    for name, b in boxes.items():
        if b[0] < 0 or b[2] < 0 or b[1] > W or b[3] > D:
            violations.append(f"{name}: outside room bounds {b}")

    # 2. zero overlap between furniture footprints (rugs live UNDER furniture)
    names = list(boxes)
    by_name = {it["name"]: it for it in items}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = by_name[names[i]], by_name[names[j]]
            if a.get("kind") == "rug" or b.get("kind") == "rug":
                continue
            ov = overlap(boxes[names[i]], boxes[names[j]])
            if ov > 1e-6:
                violations.append(
                    f"{names[i]} overlaps {names[j]} by {ov:.3f} m^2")

    # 3. walkway from doorway stays clear (doorway may sit on front or back wall)
    dw = layout.get("doorway")
    if dw:
        lane = (dw["x"] - dw["width_m"] / 2, dw["x"] + dw["width_m"] / 2)
        clear = rules["walkways"]["main_walkway_min_m"]
        back = dw.get("wall", "front") == "back"
        for name, b in boxes.items():
            near_door = b[3] > D - clear if back else b[2] < clear
            intrudes = not (b[1] < lane[0] or b[0] > lane[1])
            if near_door and intrudes:
                gap = (D - b[3]) if back else b[2]
                violations.append(
                    f"{name}: blocks doorway walkway (clearance "
                    f"{gap:.2f} m < {clear} m)")

    # 3b. door swing arc: no furniture within swing radius of the door rect
    if dw:
        swing = rules["safety"]["door_swing_clearance_m"]
        door_z = (D - 0.1, D) if dw.get("wall") == "back" else (0.0, 0.1)
        door = (lane[0], lane[1], door_z[0], door_z[1])
        for name, b in boxes.items():
            g = edge_gap(door, b)
            if 0.0 < g < swing:
                violations.append(
                    f"{name}: inside door swing arc ({g:.2f} m < {swing} m)")

    # 4. conversation zone: seat <-> coffee table gap
    # (secondary/accent seating is exempt: judged by eye, not the TV)
    cmin, cmax = rules["conversation_zone"]["sofa_to_coffee_table_m"]
    for seat in [s for s in by_kind.get("seat", []) if not s.get("secondary")]:
        for tbl in by_kind.get("table", []):
            g = edge_gap(boxes[seat["name"]], boxes[tbl["name"]])
            if g > 0 and not (cmin - 0.05 <= g <= cmax + 0.30):
                violations.append(
                    f"{seat['name']} <-> {tbl['name']}: gap {g:.2f} m "
                    f"outside conversation range [{cmin}, {cmax}] m")

    # 4b. side tables: adjacent to ANY seat (primary or accent), within arm's
    # reach (exempt from the coffee-table conversation gap by design).
    # Rev2: accent seats (e.g. recliner moved to the window wall) still get
    # side tables — measuring only against primary seats misfired.
    smax = rules.get("side_table", {}).get("max_edge_gap_to_seat_m", 0.45)
    for stbl in by_kind.get("side_table", []):
        best = None
        for seat in by_kind.get("seat", []):
            g = edge_gap(boxes[stbl["name"]], boxes[seat["name"]])
            if best is None or g < best:
                best = g
        if best is not None and best > smax:
            violations.append(
                f"{stbl['name']}: {best:.2f} m from nearest seat "
                f"(max {smax} m arm's reach)")

    # 5. TV viewing distance + facing (primary seating only)
    for seat in [s for s in by_kind.get("seat", []) if not s.get("secondary")]:
        for tv in by_kind.get("tv", []):
            cx1, cz1 = center(boxes[seat["name"]])
            cx2, cz2 = center(boxes[tv["name"]])
            dist = math.hypot(cx2 - cx1, cz2 - cz1)
            diag = tv.get("screen_diagonal_m", 0.8)
            lo = diag * rules["tv_viewing"]["distance_min_factor"]
            hi = diag * rules["tv_viewing"]["distance_max_factor"]
            if not (lo <= dist <= hi):
                violations.append(
                    f"{seat['name']} -> {tv['name']}: viewing distance "
                    f"{dist:.2f} m outside [{lo:.2f}, {hi:.2f}] m")
            fx, fz = seat.get("facing", [0, 0])
            if fx or fz:
                to_tv = (cx2 - cx1, cz2 - cz1)
                n1 = math.hypot(*to_tv)
                if n1 > 1e-6:
                    cos_a = (fx * to_tv[0] + fz * to_tv[1]) / (
                        math.hypot(fx, fz) * n1)
                    ang = math.degrees(math.acos(max(-1.0, min(1.0, cos_a))))
                    if ang > rules["tv_viewing"]["max_off_axis_deg"]:
                        violations.append(
                            f"{seat['name']} faces {ang:.0f}deg off the TV "
                            f"(max {rules['tv_viewing']['max_off_axis_deg']:.0f}deg)")

    if violations:
        print("LAYOUT INVALID:")
        for v in violations:
            print("  - " + v)
        return 1
    print(f"LAYOUT OK: {len(items)} items, all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
