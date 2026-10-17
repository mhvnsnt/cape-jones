# Aider lane conventions (cape-jones)

How OUR lanes use aider. The repo's AGENTS.md laws apply in full —
especially VERIFY-BEFORE-CLAIMING and CHECK-BEFORE-START. This doc is the
aider-specific layer on top.

## 1. Always on a worktree branch off origin/main. Never on main.

```bash
cd ~/workspace/cape-jones
git worktree add ~/workspace/cape-jones-<lane>-<date> origin/main
cd ~/workspace/cape-jones-<lane>-<date> && git checkout -b <lane>/<what>-YYYYMMDD
```

Run aider from the worktree root so it picks up `.aider.conf.yml` automatically.
Do NOT touch `.vscode/` (another lane owns it) or another lane's branch
(e.g. `build/living-room-relayout-20261016`).

## 2. Check before you start

Before launching aider on a file, check no other lane is already iterating on it:
`git branch -a`, the lane checkpoints, recent commits. Duplicate aider sessions on
the same files burn quota and collide.

## 3. Aider's diffs get eyes before anything else

1. `git diff` — read every hunk yourself.
2. Compile / validate: `python3 -m py_compile <file>`,
   `python3 tools/layout-rules/validate_layout.py 3d-assets/living_room_layout.json` where relevant.
3. Only then: `git add` + deliberate commit, push, PR, verify green/mergeable, merge.
   `auto-commits` is OFF in the repo config for this reason — aider must never
   commit on its own.

## 4. What aider does and doesn't touch

- YES: Python scripts, JSON configs, docs, shell glue, tests.
- NO: `.blend` scene files (binary — aider can't see them; `.aiderignore` excludes
  them). Scene changes go through the deterministic scripts
  (`tools/layout-rules/apply_layout_blend.py`), which aider MAY iterate on.
- Add big context as read-only: `aider --read <file>` adds it to chat without
  letting aider edit it.

## 5. Non-interactive lane runs

- First run of a new task: interactive (or omit `--yes-always`) so you see the
  plan. Repeat runs can use `--message "..." --yes-always`.
- One aider session per worktree at a time (git state + watch-files).

## 6. Keys and privacy

- Keys live in env vars only (`GEMINI_API_KEY`). Never in files, logs, chat, or PRs.
- `analytics-disable: true` is set in the repo config; leave it.
- The stored `custom.legacy-gemini` connector credential is for one-turn image
  edits and is NOT an aider key — do not try to extract it.

## 7. Reporting

Tag evidence per AGENTS.md: `verified` (2+ independent sources, checked yourself),
`single-source`, `unverified`, `contradicted`. "Aider ran" is a claim — the diff
you read with your own eyes is the evidence.
