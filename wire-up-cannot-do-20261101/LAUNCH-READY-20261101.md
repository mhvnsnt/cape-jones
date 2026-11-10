# HARMONY LAUNCH — READY TO RUN THE MINUTE A LICENCE SHOWS
Account: fmmg.mars@gmail.com ONLY. No card entry by any agent, no purchase,
no Windows .exe, no Mac .dmg, no third-party/crack site.
Blocker today (2026-11-01): no trial licence on the shop account
(last parent browser check 11:57 CST: no subscription, no licence, no order),
and no Linux .tgz on disc. Harmony is NOT working until a binary launches.

## Step 1 — recheck the shop (parent, live browser)
shop.toonboom.com/en/subscriptions and /en/downloads.
If a licence appears, note edition + start + end dates. Do not proceed
on a licence that is not there.

## Step 2 — download Linux only
HAR27-PRM-lnx-25340.tgz, from the customer portal / Linux try route.
Verify on disc: file <name> (gzip), size >100MB, sha256 logged.

## Step 3 — install in Rocky 9 chroot
bash ~/workspace/toon-boom-linux-20261101/install-harmony-rocky-chroot-v2.sh /path/to/HAR27-PRM-lnx-25340.tgz
Or, if the file lands in a watched dir, the watcher does this:
bash ~/workspace/toon-boom-linux-20261101/watch-for-harmony.sh
Inside the chroot: tar -xvzf, then ./install, choose STANDALONE.

## Step 4 — License Wizard + launch
/usr/local/ToonBoomAnimation/harmony[Edition]_27/lnx86_64/bin/LicenseWizard
Sign in as fmmg.mars@gmail.com. Launch via host Xvfb (display :99 was
prepared in toon-boom-linux-20261101/work/).

## Step 5 — first Harmony proof, in order
1. Open the exporter prototype: exporter/CapeJonesToon.tpl
   (record: opens / fails, with the exact error, no guessing)
2. Render one frame in Harmony
3. Only then claim in-Harmony rendering, .tpl import, or .plt import
Scripts syntax-checked 2026-11-01 (bash -n, all pass). RAM note: VM has
7.7GB, Harmony minimum is 8GB — swap on /home is the next step if the
installer complains, not a reason to claim it works without a launch.
