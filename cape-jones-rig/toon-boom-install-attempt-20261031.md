# Toon Boom Harmony install attempt — Muse's side (Linux VM)
Date checked: 2026-10-31 (Sat, America/Chicago), subagent report to parent.
Account in scope: fmmg.mars@gmail.com ONLY. marquiswhitacre@gmail.com must NOT be used (rejected by Toon Boom, "unrecognized username or password").

## Verdict, plainly
- Harmony is NOT installed on this VM. No installer file was found locally, no install was run, no activation happened in this check.
- Trial: NOT confirmed. Edition, start date, and end date are still unconfirmed from the account.
- Download: NOT confirmed. Mars's 2026-10-31 20:15 CDT report ("card entered, trial started, processing your download request") is the only evidence, and the earlier browser re-check found only "Processing your download request" — no edition/start/end/price, and no trial info on the account Overview page.
- This is NOT a final stop: the exact unblocker and the free ways around it are below.

## What this VM actually is (measured, not assumed)
- Ubuntu 24.04.5 LTS, kernel 7.0.0-39-generic, x86_64
- 4 CPUs, 7.7 GB RAM (Harmony minimum is 8 GB), 58 GB free on /home
- No Wine / Wine64, no VirtualBox / VBoxManage, no QEMU, no /dev/kvm found
- No Toon Boom installer in ~/workspace/tools-industry or ~/Downloads; only the reminder file TOON-BOOM-TRIAL-REMINDER-20261031.md exists locally

## Why a native install cannot run here
- Toon Boom's own Harmony 27 system requirements list workstations as Windows 10/11 (64-bit) and macOS only (macOS 15.3 Sequoia / 14.6 Sonoma / 13.6.7 Ventura / 12.7.3 Monterey, plus newer Tahoe listings). No Linux workstation build is listed.
- The Linux listings are for Harmony SERVER only (CentOS Stream 9 / Rocky Linux 9.4), not the standalone Harmony workstation Mars wants. This VM is Ubuntu 24.04, not CentOS/Rocky, so even the server build is not a match.
- Sources: docs.toonboom.com Harmony 27 system requirements; Toon Boom trial activation docs.

## Trial-clock point that changes the reminder math
- Per Toon Boom's trial activation docs: a trial lasts 21 days starting from the day it is ACTIVATED — i.e. after installing, launching, and signing in at the activation prompt — not from the download-request date.
- The local reminder file counts 14 days from 2026-10-31 (day 11 = 2026-11-11, day 13 = 2026-11-13, end ~2026-11-14) and itself says the end date and edition were NOT confirmed. Those two counts disagree (14 vs 21 days, and download vs activation start). Do NOT state either end date as confirmed until the account is checked. The armed reminders should be shifted once a real activation date is confirmed — that is the standing shift rule, and it has not been triggered yet because activation has not been confirmed.

## Free ways around, evaluated honestly (none claimed as done)
1. Wine / Bottles on this VM — community reports are mixed and old: WineHQ has no Harmony 27 listing; Harmony 15 had a Wine bug (missing/unimplemented tbs.dll function) and Harmony 20 had a project-open bug under Bottles. Even if Wine were installed, there is still no Harmony installer file in hand, and activation through Wine is the likeliest failure point. Next step if the installer is obtained: install Wine/Bottles, run the installer, and test activation — expect it to be an experiment, not a guaranteed install.
2. Windows VM (VirtualBox/QEMU) on this VM — no hypervisor installed, no /dev/kvm, and 4 CPU / 7.7 GB RAM is below Harmony's 8 GB minimum before Windows itself takes its share. A Windows 11 VM here would be slow to unusable, and a Windows licence/ISO is still needed. Not recommended on this VM.
3. Cloud Windows desktop (e.g. Azure dev/test Windows 11 images, or a cloud provider's free-trial VM) — technically the cleanest real Windows install path, but it needs a NEW cloud account / sign-in decision from Mars. I did not create one, invent credentials, or start a paid/trial cloud account. That is a Mars decision, not a silent step.
4. Harmony Server on Linux — wrong tool (server/database only, CentOS/Rocky only), not the standalone workstation.
5. What IS runnable now, free, already on this VM: Tahoma2D 1.6.3, Blender 5.2.3, Krita, Pencil2D, Synfig (in ~/workspace/tools-industry). These are not Harmony, but they are the working animation tools available today while Harmony is unblocked.

## Exact unblocker — what the parent/root must delegate (browser task, not a generic subagent)
A live-browser task, signed in with the saved Secure Vault login for toonboom.com, account fmmg.mars@gmail.com ONLY, must:
1. Open the Toon Boom account Overview / Manage My Subscriptions and record: trial edition (Essentials/Advanced/Premium), trial start date, trial end/expiration date, and whether a trial licence exists on the account at all.
2. Press Download on the product page (Toon Boom's own docs say pressing Download is the action that activates the trial on the account) and save the installer, recording the exact installer filename/version.
3. Only then can a Wine attempt (step 1 above) or a cloud-Windows install (step 3 above) be attempted with a real installer in hand.
No purchase, no card entry, no cancellation was done or attempted in this check, and none should be done without Mars's explicit approval for that specific step.

## What was NOT done
- No sign-in to Toon Boom (subagents cannot do live-browser sign-ins; no website visit is claimed from a text search).
- No download, no install, no activation, no Wine install (installing Wine without an installer would prove nothing about Harmony).
- No change to the armed trial reminders and no repo push (the reminder file needs updating only after a confirmed activation date, then PR-only).
- The prohibited marquiswhitacre@gmail.com account was not used or retried.

## Status for Mars
- Install confirmation: approval 0/1, NOT approved — nothing is installed to confirm.
- Trial confirmation: 0/1, NOT confirmed — edition/start/end still unknown from the account.
- Next action belongs to the parent: delegate the browser check above, or ask Mars to confirm the trial details from his Toon Boom account page / confirmation email.
