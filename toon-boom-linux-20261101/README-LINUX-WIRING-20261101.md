# Toon Boom Harmony on GNU/Linux — wiring, 2026-11-01

## What is in this folder
- `ROUTE-REPORT-20261101.md` — Rocky Linux 9.8 chroot route, tested, Harmony binary NOT yet launched.
- `install-harmony-rocky-chroot.sh` — rebuilds the Rocky rootfs from the container tarball if /root was wiped, re-copies hosts/resolv/CA, re-installs deps, copies a Harmony Linux .tar.gz into /root in the chroot, extracts it, and runs the installer interactively.
- `rocky9-container.tar.xz.part-00` … `part-03` — the 83 MB Rocky 9 container tarball, split into 25 MB chunks because the GitHub Contents API ceiling here sits between 36 MB (worked) and 51 MB (failed). Reassembling the chunks reproduces the original file byte-for-byte.

## Reassemble the Rocky container tarball
```bash
cat rocky9-container.tar.xz.part-00 rocky9-container.tar.xz.part-01 \
    rocky9-container.tar.xz.part-02 rocky9-container.tar.xz.part-03 \
    > rocky9-container.tar.xz
sha256sum rocky9-container.tar.xz
# expected: 1210df99dcf0ef4d73940244e6d703935175629598b09c0e430da20e76768402
```

## Install Harmony on Linux, once the Harmony .tar.gz lands
Harmony on Linux does NOT use an .exe — .exe is Windows only. Linux is a .tar.gz archive with an installation script.

```bash
tar -xvzf HAR27-PRM-lnx-25340.tgz
cd <extracted-folder>
sudo ./install        # whiptail/newt interactive installer
# choose: Standalone, NOT Server/Client
```

Then activate with the License Wizard, signed in as fmmg.mars@gmail.com only:
```
/usr/local/ToonBoomAnimation/harmonyPremium_27/lnx86_64/bin/LicenseWizard
```

Or, on this VM, run the chroot wrapper (it does the Rocky rebuild, deps, copy, extract, and install):
```bash
./install-harmony-rocky-chroot.sh HAR27-PRM-lnx-25340.tgz
```

## Still owed, NOT in this folder, NOT claimed as landed
- The Harmony Linux installer itself, `HAR27-PRM-lnx-25340.tgz` — not on disc, not in this repo. The Toon Boom shop account for fmmg.mars@gmail.com showed 0 subscriptions / 0 orders / 0 licenses, and the Linux CDN route returned AccessDenied (4th attempt, 2026-11-01). A trial submission by Mars was still showing "Processing your download request" at last check.
- A launched Harmony binary, a verified GUI launch, and a trial edition/start/end date.
- Blockers carried from the route report: VM RAM 7.7 GB vs 8 GB minimum (add swap before a GUI launch), no GPU (llvmpipe/swrast software GL only), no full GNOME set in the chroot, /tmp was 100% full at test time.

## No donor art in this batch
This batch contains no donor character art, design, logo, name, or dialogue. The standing placeholder rule (Mars, 2026-11-01 11:50 CST, repo owner): donor art may be used only as a marked TEMPLATE-PLACEHOLDER, wired into rig tests, then transformed into a completely different original — never shipped as-is in a final deliverable.
