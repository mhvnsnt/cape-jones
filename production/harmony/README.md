# Toon Boom Harmony — Linux wiring (2026-11-05)

**Owner directive (2026-11-05): Toon Boom Harmony runs on Linux. Find the install; never write "Linux unsupported" or "Windows/Mac only".**
Harmony 27 has a native GNU/Linux build (see `cape-jones-rig/toon-boom-10-ways-20261101/10-WAYS-REPORT-20261101.md`):
a `.tar.gz` -> `./install` (choose STANDALONE) -> `LicenseWizard`. Toon Boom lists CentOS Stream 9 / Rocky 9.4; other distros are "may not run properly", not "cannot".
The Windows file the owner downloaded twice (`HAR27-PRM-win-25340.exe`, 656 MB) is the wrong installer for Linux.
Account: fmmg.mars@gmail.com ONLY. No pirated copies, no licence bypass.

| File | What it does |
|---|---|
| `find_harmony.sh` | Searches `/usr/local/ToonBoomAnimation /opt $HOME /workspace /tmp /mnt /media` (override `HARMONY_SEARCH_ROOTS`, or set `HARMONY_BIN`). exit 0 = binary, 2 = Linux tarball only, 1 = nothing. |
| `install_harmony_linux.sh <tar.gz>` | SHA-256s the owner's tarball, installs deps (apt or dnf), runs Toon Boom's `./install`, points to LicenseWizard. |
| `harmony_stage.py [scene.xstage]` | Pipeline stage. Binary present -> `HarmonyPremium -batch -scene <xstage>` (renders Write nodes). Absent -> runs Cape Jones Toon (`cape-jones-rig/toon-boom-own-version-20261101`) and labels the result **NOT Harmony**. |

Launch once installed: `/usr/local/ToonBoomAnimation/harmonyPremium_27/lnx86_64/bin/HarmonyPremium` (GUI, needs a desktop/GNOME session) or batch as above.

## Search log, 2026-11-05 (Grok Bot executor, box Debian 13, 8 CPU, 15 GB RAM)
- Box: `find / -xdev` for `*harmony*`, `*toonboom*`, `*toon-boom*`, `HAR2*`, `*harmony*.tar*`, `*harmony*.exe`, `LicenseWizard`; `/usr/local/ToonBoomAnimation`; `~/.wine*`, `/opt/wine*`; `which wine harmony HarmonyPremium` -> **no Harmony binary, no Linux tarball, no .exe on this box.** Only repo notes.
- Google Drive (owner connector): name contains HAR2 / Harmony / ToonBoom / Toon Boom -> **no results.**
- Owner's other machines: only an Android phone (offline). Muse's Ubuntu VM (where the .exe was downloaded) is not reachable from this box.
- Result: `find_harmony.sh` -> `HARMONY_BIN=NOT_FOUND`. `harmony_stage.py` -> Cape Jones Toon fallback, exit 0 (19 nodes, 6 chains, round-trip exact).
- Unblocker: download **Harmony 27 Premium — GNU/Linux** tarball from the Toon Boom account (fmmg.mars@gmail.com) to this box, then `sudo bash production/harmony/install_harmony_linux.sh <file>`, then LicenseWizard sign-in (owner).
