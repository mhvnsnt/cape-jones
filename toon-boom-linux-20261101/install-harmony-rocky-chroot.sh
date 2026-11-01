#!/bin/bash
# Toon Boom Harmony on this Linux VM — Rocky 9 chroot route, prepared 2026-11-01
# DO NOT RUN until the Harmony Linux .tar.gz is on disc (browser task, fmmg only).
# No purchase, no card entry, no Azure in this script. Account: fmmg.mars@gmail.com ONLY.
# Usage:  ./install-harmony-rocky-chroot.sh /path/to/Harmony-27-*.tar.gz
set -e
PKG="$1"
[ -n "$PKG" ] || { echo "usage: $0 <harmony-linux-tar.gz>"; exit 2; }
[ -f "$PKG" ] || { echo "tar.gz not found: $PKG"; exit 2; }

# 1. Rocky 9 rootfs, already prepared: podman vfs storage at /root/pvfs
#    If /root/pvfs is gone (VM reset), rebuild it first:
#      podman --storage-driver=vfs --root /root/pvfs --runroot /root/prun \
#        load -i ~/workspace/toon-boom-linux-20261101/rocky9-container.tar.xz
R=$(ls -d /root/pvfs/vfs/dir/*/ 2>/dev/null | head -1)
[ -n "$R" ] || { echo "Rocky rootfs not found at /root/pvfs — rebuild from rocky9-container.tar.xz first"; exit 2; }
echo "Rocky rootfs: $R"
cat "$R/etc/os-release" | head -3

# 2. Host network inside chroot: copy host hosts/resolv.conf + egress CA.
#    Do NOT hardcode proxy credentials in this script: use the proxy env
#    variables already provided by the runtime environment.
cp /etc/hosts "$R/etc/hosts"
cp /etc/resolv.conf "$R/etc/resolv.conf"
cp /usr/local/share/ca-certificates/hatch-egress-ca.crt \
   "$R/etc/pki/ca-trust/source/anchors/" 2>/dev/null || true

# 3. Harmony dependencies (verified installed 2026-11-01, Rocky 9.8):
#    newt (provides whiptail), libX11, libXext, libXrandr, alsa-lib, libSM,
#    fontconfig, libjpeg-turbo, libpng, libXi, libxkbcommon, libxkbcommon-x11,
#    libglvnd-opengl, initscripts, mesa-libGLU, sdl12-compat, pcre2-utf16,
#    xcb-util-keysyms, xcb-util-renderutil, xcb-util-image, xcb-util-wm,
#    chkconfig, mesa-dri-drivers (swrast / llvmpipe software GL).
chroot "$R" /bin/bash -c '
  export https_proxy="$HTTPS_PROXY" http_proxy="$HTTP_PROXY" HTTPS_PROXY="$HTTPS_PROXY" HTTP_PROXY="$HTTP_PROXY"
  update-ca-trust extract || true
  dnf install -y newt libX11 libXext libXrandr alsa-lib libSM fontconfig \
    libjpeg-turbo libpng libXi libxkbcommon libxkbcommon-x11 libglvnd-opengl \
    initscripts mesa-libGLU sdl12-compat pcre2-utf16 \
    xcb-util-keysyms xcb-util-renderutil xcb-util-image xcb-util-wm \
    chkconfig mesa-dri-drivers
  rpm -q newt whiptail 2>/dev/null || true; ls -l /usr/bin/whiptail
'

# 4. Unpack Harmony and run the installer, STANDALONE (not Server/Client).
#    The installer is interactive (whiptail) and asks to review/agree the
#    licence. Run it in a terminal, not headless, the first time.
cp "$PKG" "$R/root/"
chroot "$R" /bin/bash -c '
  cd /root && tar -xvzf ./"$(basename "$PKG")"
  echo "Unpacked. Now run, interactively, inside chroot:"
  echo "  cd /root/<harmony-package-dir> && ./install"
  echo "Choose STANDALONE when prompted."
  echo "If not activated, launch License Wizard afterwards:"
  echo "  /usr/local/ToonBoomAnimation/harmony[Edition]_27/lnx86_64/bin/LicenseWizard"
'
echo "Next: run ./install inside the chroot, choose STANDALONE, then License Wizard as fmmg.mars@gmail.com."
echo "Blockers still open at script time: licence/trial on the account, 7.7 GB RAM < 8 GB minimum, no GPU (llvmpipe software GL only), no GNOME in chroot (X display via host Xvfb, needs free /tmp)."
