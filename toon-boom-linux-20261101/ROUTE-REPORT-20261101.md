# Toon Boom Harmony on this Linux VM — reverse-engineered / free route, 2026-11-01

Mars, 2026-11-01 11:17 CST: find a way, or reverse-engineer one, get into the
Toon Boom account, card information already given to Toon Boom by Mars himself.
No purchase, no card entry, no Azure in this task. Account: fmmg.mars@gmail.com ONLY.
Browser task (parent) is checking the account / Linux .tar.gz separately — no
sign-in was done here.

## Route chosen: Rocky Linux 9.8 chroot on the Ubuntu VM — TESTED, Harmony itself NOT yet launched

This is the first route on this VM that actually boots a supported Rocky 9
environment. It is NOT a claim that Harmony works — no Harmony binary has run
yet, because the Linux .tar.gz is not on disc (see blocker 1).

### What was tested, with results
- Host VM: Ubuntu 24.04.5 LTS, 4 CPU, 7.7 GB RAM total (available ~0.6–2.0 GB
  during tests, 0 swap), 55 GB free on /home, /tmp 512 MB tmpfs 100% full
  (other agents' flashcheck scratch, not deleted here), no /dev/kvm,
  no vmx/svm, no /dev/dri, no GPU.
- Software GL, PROVEN: Mesa llvmpipe (LLVM 20.1.2, 256 bits) via EGL swrast
  on the host (`eglinfo`), and Blender 4.5.3/5.2.3 already rendered headless
  with EEVEE after libegl1/libgl1. Host also has whiptail, libnewt, Xvfb.
- Rocky 9 image: `Rocky-9-Container-Base.latest.x86_64.tar.xz`, 83 MB,
  downloaded from dl.rockylinux.org, loaded with podman 4.9.3 (installed
  free via apt) as `localhost/rockylinux:9`, 244 MB, Rocky Linux 9.8 (Blue Onyx).
- Routes that FAILED, in order, with the exact failure:
  1. podman run, default overlay driver: fuse device not found
     (`fuse-overlayfs: cannot mount: No such file or directory`), because
     this restricted VM has no /dev/fuse.
  2. podman run, vfs driver, default storage: database graph-driver mismatch
     (first load used overlay); fixed by a separate vfs root at /root/pvfs.
  3. podman run, vfs driver, /root/pvfs: crun `cannot open sd-bus`.
  4. systemd-nspawn on the podman rootfs: `Failed to mount sysfs … Operation
     not permitted` — no CAP_SYS_ADMIN in this VM.
  5. Hand-extracting the OCI layer tar to ~/workspace: partial only.
     Symlink/ownership errors on the overlay workspace mount; podman vfs
     extraction is the canonical rootfs, not the hand extract (deleted).
- Route that WORKS: plain `chroot` into the podman vfs rootfs
  (`/root/pvfs/vfs/dir/<id>/`, 585 MB with deps). No mounts, no KVM, no fuse,
  no sd-bus needed. Inside chroot: `cat /etc/os-release` = Rocky Linux 9.8,
  `dnf --version` = 4.14.0. This is the reverse-engineered fit: Rocky
  userspace on the Ubuntu kernel, same x86_64, no VM, no container runtime
  mount privileges required.
- Network inside chroot, FIXED by two steps: copy host /etc/hosts +
  /etc/resolv.conf into the chroot, and copy the host egress CA
  (`hatch-egress-ca.crt`) into `/etc/pki/ca-trust/source/anchors/` +
  `update-ca-trust extract`. Before the CA step, dnf failed with
  `SSL certificate problem: self-signed certificate in certificate chain`;
  after it, dnf works. Proxy credentials are NOT written in any file here —
  the script reuses the runtime's proxy environment variables.
- Harmony dependencies, INSTALLED and verified inside the Rocky chroot
  (Toon Boom docs, Harmony 24 Linux dependency page):
  newt 0.52.21-11.el9 (provides /usr/bin/whiptail — the installer prerequisite),
  libX11, libXext, libXrandr, alsa-lib, libSM, fontconfig, libpng, libXi,
  libxkbcommon, libglvnd-opengl, mesa-libGLU, sdl12-compat, pcre2-utf16,
  xcb-util-keysyms, xcb-util-renderutil, xcb-util-image, xcb-util-wm,
  initscripts, chkconfig, mesa-dri-drivers (swrast_dri.so, libGL.so.1).
  libjpeg in the docs = libjpeg-turbo 2.0.90 in Rocky, already present
  as a dependency. WebCC/rabbitmq-server is NOT installed — only needed
  for a Server/WebCC setup, and this route is STANDALONE, so it is skipped.

## What happens the minute the .tar.gz lands
Script: `install-harmony-rocky-chroot.sh <harmony-linux-tar.gz>`
1. Re-check Rocky rootfs at /root/pvfs (rebuild from the 83 MB tar.xz in
   this folder if a VM reset wiped /root).
2. Re-copy hosts/resolv.conf/CA, re-run the dependency install (idempotent).
3. Copy the .tar.gz into /root inside the chroot, `tar -xvzf`, `cd` into
   the package dir, run `./install` INTERACTIVELY (whiptail), choose
   STANDALONE (not Server/Client), review/agree the licence in the installer.
4. If not activated, launch License Wizard:
   `/usr/local/ToonBoomAnimation/harmony[Edition]_27/lnx86_64/bin/LicenseWizard`
   and sign in as fmmg.mars@gmail.com. That step, plus the account trial
   state, is what the parent browser task is checking.

## Exact blockers, in order — none hidden
1. **No Linux .tar.gz on disc.** Browser task separate. Shop previously
   showed 0 subscriptions / 0 orders / 0 licenses for fmmg, so no Linux
   link was offered. If the browser task finds a trial link, this route
   can proceed; if it finds no trial, the trial was never started and
   only Mars's own trial start (or a product code) on the account fixes it.
   Card information Mars gave Toon Boom himself does not, by itself,
   create a trial licence — the account page must show one.
2. **RAM below minimum.** Harmony minimum is 8 GB; this VM has 7.7 GB
   total, ~0.6–2.0 GB available at test time, 0 swap. The License Wizard
   (first test) may run; a full Harmony GUI render may OOM. Mitigation
   tried: none yet — adding swap is possible on /home (55 GB free) and is
   the next step before a GUI launch, not done here because no Harmony
   binary exists to test against yet.
3. **No GPU, proprietary-driver requirement unmet.** Toon Boom docs
   require official proprietary GPU drivers; Nouveau/Mesa routinely crash
   or display-bug per docs. Here the only GL is llvmpipe software
   rendering (host) and mesa swrast (Rocky). It may run slowly, or
   Harmony may refuse/crash on software GL — untested until a binary runs.
4. **No GNOME, no X display ready.** The chroot is a minimal container
   plus deps, not the full GNOME Desktop set Toon Boom recommends, and
   host Xvfb cannot start while /tmp is 100% full. GUI test needs:
   free /tmp, host Xvfb, DISPLAY passed into chroot, then License Wizard.
   Headless `--help` / License Wizard CLI check, if any, comes first.
5. **Podman rootfs location is outside the workspace.** /root/pvfs
   (585 MB) may not survive a VM reset the way ~/workspace does. The
   83 MB Rocky tar.xz in this folder IS the durable rebuild source.

## Fastest real route, alongside the VM route (state plainly, do not hide it)
Mars's own Windows/Mac, with the already-downloaded
`HAR27-PRM-win-25340.exe` (656 MB, 2 copies in his own Downloads, NOT on
this VM): run it there, sign in as fmmg at the License Wizard — that IS
the trial start, and Mars reports edition/start/end back. That route
needs no Rocky container, no RAM/GPU fight, and no new download. The
VM chroot route above is now prepared, but it is NOT faster than that
until blockers 1–4 clear.

## What runs TODAY (Harmony-compatible workflow, NOT Harmony itself)
Blender 4.5.3/5.2.3 LTS, Tahoma2D 1.6.3 (extracted binary), and
Cape Jones Toon (`cjtoon.py`, 19 nodes, FK 6/6, .cjstage round-trip
19/19, re-tested 2026-11-01) with Harmony cut-out hierarchy/peg/pivot
data (forearm child of arm, hand child of forearm). This produces work
now. It does NOT prove in-Harmony rendering, .tpl/.plt export, or
activation, and is never claimed as Harmony.

## Files in this folder
- [rocky9-container.tar.xz](sandbox://workspace/toon-boom-linux-20261101/rocky9-container.tar.xz) — Rocky 9 container base, 83 MB, durable rebuild source
- [install-harmony-rocky-chroot.sh](sandbox://workspace/toon-boom-linux-20261101/install-harmony-rocky-chroot.sh) — install script, run only when .tar.gz lands
- [ROUTE-REPORT-20261101.md](sandbox://workspace/toon-boom-linux-20261101/ROUTE-REPORT-20261101.md) — this report
- Partial hand-extract folders deleted (regenerable from the tar.xz).
- Podman vfs root at /root/pvfs (outside workspace, 585 MB) and podman-vfs
  scratch dir in this folder are NOT deliverables; the tar.xz + script are.
