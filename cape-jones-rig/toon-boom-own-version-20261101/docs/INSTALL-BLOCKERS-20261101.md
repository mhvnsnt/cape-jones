# Install Blockers — Toon Boom Harmony, browser attempt (not duplicated here)

This job is research/build. The browser install attempt is a SEPARATE
browser task, already waiting on Mars takeover (tab t1 left open).
Do NOT duplicate browser work here; this file records the blockers so
the next browser attempt does not repeat them.

## Blockers, in order

1. **OS mismatch — the hard blocker.** This browser/VM environment is
   Linux. Installer HAR27-PRM-win-25340.exe, 656 MB, is a Windows .exe
   (Harmony 27 Premium, Windows). Toon Boom's official Harmony page
   lists System Requirements only for Windows 11 / Windows 10 (64-bit)
   and macOS — no Linux option, no browser-based Harmony.
   A Windows .exe cannot be run natively in this Linux browser.

2. **Downloads UI not reachable via automation.** Browser task tried:
   Ctrl+J twice (reported applied, page view did not navigate, screenshot
   shows only page content, not toolbar/Downloads popup); clicking the
   Downloads button in the top-right toolbar (not sent: grounding view
   said toolbar is not visible in screenshot, only webpage content);
   chrome://downloads (refused: browser tool accepts only http/https URLs).
   Result: HAR27-PRM-win-25340.exe presence in Downloads was NOT
   independently re-verified in that session; location is as supplied
   from Mars's earlier screenshots.

3. **Subscription NOT confirmed.** Shop pages at last check: 0 subscriptions,
   0 orders, 1 Visa ending 3493 on file, account fmmg.mars@gmail.com only.
   Mars's claim 2026-11-01 01:28 CST ("paid subscription, we own it") is
   recorded, NOT confirmed. Download ≠ activation. Activation = install
   + launch + sign-in on Windows/Mac, then the app itself shows
   edition/subscription/start/end.

## Workarounds tried

- Browser Downloads UI via shortcut, toolbar click, chrome:// URL: all
  failed as above, for automation-view reasons, not for lack of trying.
- Linux install via Wine/VirtualBox/QEMU/KVM: NOT used, per standing
  rule for this VM; Harmony is not claimed installed on Linux.
- Browser-based Harmony alternative: none found on toonboom.com;
  Toon Boom Producer is production management, not a Harmony substitute.

## Workaround that would work

On a Windows 10/11 (64-bit) computer — or a Mac, using the Mac installer
instead — copy HAR27-PRM-win-25340.exe to that machine, run it there,
launch Harmony, sign in only as fmmg.mars@gmail.com, activate, and
record what the app shows. Do NOT start a third download; the (1) copy
is the same installer, 2 downloads, 0 charges per site text.
No purchase, no card entry by an agent.

## What our own version does NOT need Harmony installed to do

Everything in cjtoon.py + build_own_version.py (exit 0): load, validate,
inbetween, onion skin, palette, .cjstage round-trip, Harmony check-script
generation. Harmony is needed only for in-app verification, .tpl/.plt
export, and in-Harmony rendering.
