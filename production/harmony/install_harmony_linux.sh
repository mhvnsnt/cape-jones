#!/usr/bin/env bash
# Install the owner's Harmony GNU/Linux tarball (never a pirated copy). Usage: install_harmony_linux.sh HAR27-...tar.gz
# Follows Toon Boom's documented Linux flow: extract -> ./install (choose STANDALONE) -> License Wizard.
set -euo pipefail
TAR="${1:?path to the owner's Harmony Linux .tar.gz}"
sha256sum "$TAR" | tee "$(dirname "$TAR")/$(basename "$TAR").sha256"
W=$(mktemp -d /tmp/harmony-install-XXXX); tar -xzf "$TAR" -C "$W"
# documented deps (CentOS/Rocky names in docs; Debian/Ubuntu equivalents):
if command -v apt-get >/dev/null; then apt-get install -y whiptail libx11-6 libxext6 libxrandr2 libasound2t64 libsm6 fontconfig libjpeg62-turbo libpng16-16 libxi6 libxkbcommon0 libglvnd0 libsdl2-2.0-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 || true
elif command -v dnf >/dev/null; then dnf install -y newt libX11 libXext libXrandr alsa-lib libSM fontconfig libjpeg libpng libXi libxkbcommon libglvnd-opengl chkconfig SDL xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil || true; fi
INSTALLER=$(find "$W" -maxdepth 3 -name install -type f | head -1)
echo "Running $INSTALLER — choose STANDALONE, accept the licence."; (cd "$(dirname "$INSTALLER")" && ./install)
echo "Then activate: /usr/local/ToonBoomAnimation/harmonyPremium_27/lnx86_64/bin/LicenseWizard (sign in as fmmg.mars@gmail.com)"
