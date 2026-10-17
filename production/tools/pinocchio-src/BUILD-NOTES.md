# Pinocchio source — build notes (this lane)

- Mirror: https://github.com/jingma-git/Pinocchio (shallow clone, 2026-10-17).
  Original: Ilya Baran, MIT CSAIL ("Automatic Rigging and Animation of 3D
  Characters", SIGGRAPH 2007). Library = **LGPL-2.1** (see `README.txt`
  "LICENSING" section in this dir); the `DemoUI` demo = MIT.
- The original MIT download page is offline (404 as of 2026-10-17); this
  mirror is the surviving source of the canonical code.

## g++ ≥ 11 build fixes (2 one-line changes, build-only)

Old code relied on a lax friend lookup: inside namespaces `_VectorPrivate`
/ `_RectPrivate`, `friend class Vector;` / `friend class Rect;` bound to a
nonexistent namespaced class instead of the global `::Vector` / `::Rect`,
so every call to the private static helpers failed with
"is private within this context" on g++ 11+ (Ubuntu 24.04 ships g++ 13).

- `Pinocchio/vector.h`: `friend class Vector;` → `friend class ::Vector;`
- `Pinocchio/rect.h`:   `friend class Rect;`   → `friend class ::Rect;`
  (inside the `RectOp` helper only; the other friend line needed no change)

Build:
```bash
cd Pinocchio && make        # -> libpinocchio.a
```
No other source changes. `Demo/` / `DemoUI/` (FLTK GUI) were not built —
this lane uses the headless `rig.cpp` driver in `../pinocchio/` instead.
