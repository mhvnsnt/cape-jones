#!/usr/bin/env bash
# Cape Jones — locate a Toon Boom Harmony install or installer on THIS machine.
# Harmony 27 ships a native GNU/Linux build (.tar.gz -> ./install -> STANDALONE -> LicenseWizard).
# Officially listed distros: CentOS Stream 9 / Rocky Linux 9.4; owner directive 2026-11-05:
# Harmony runs on Linux — find the install, never write "Linux unsupported".
# Prints KEY=VALUE lines; exit 0 if a runnable binary is found, 2 if only an installer, 1 if nothing.
set -u
ROOTS="${HARMONY_SEARCH_ROOTS:-/usr/local/ToonBoomAnimation /opt $HOME /workspace /tmp /mnt /media}"
BIN=""; for r in $ROOTS; do [ -d "$r" ] || continue
  b=$(find "$r" -maxdepth 7 -type f \( -name 'HarmonyPremium' -o -name 'HarmonyAdvanced' -o -name 'HarmonyEssentials' \) -perm -u+x 2>/dev/null | head -1)
  [ -n "$b" ] && { BIN="$b"; break; }; done
[ -z "$BIN" ] && [ -n "${HARMONY_BIN:-}" ] && [ -x "$HARMONY_BIN" ] && BIN="$HARMONY_BIN"
INST=$(for r in $ROOTS; do [ -d "$r" ] && find "$r" -maxdepth 5 -type f \( -iname 'HAR2*lnx*.tar*' -o -iname 'HAR2*linux*.tar*' -o -iname 'HAR2*.tar.gz' -o -iname '*harmony*linux*.tar*' \) 2>/dev/null; done | head -1)
WINEXE=$(for r in $ROOTS; do [ -d "$r" ] && find "$r" -maxdepth 5 -type f -iname 'HAR2*-win-*.exe' 2>/dev/null; done | head -1)
if [ -n "$BIN" ]; then
  echo "HARMONY_BIN=$BIN"; echo "HARMONY_FILE=$(file -b "$BIN" | cut -c1-80)"
  echo "LICENSE_WIZARD=$(dirname "$BIN")/LicenseWizard"; exit 0; fi
[ -n "$INST" ] && { echo "HARMONY_LINUX_INSTALLER=$INST"; echo "NEXT=sudo bash production/harmony/install_harmony_linux.sh '$INST'"; exit 2; }
[ -n "$WINEXE" ] && echo "HARMONY_WINDOWS_EXE=$WINEXE  # wrong installer for Linux; download the GNU/Linux .tar.gz from the Toon Boom account (fmmg.mars@gmail.com)"
echo "HARMONY_BIN=NOT_FOUND"; echo "SEARCHED=$ROOTS"
echo "NEXT=download Harmony 27 Premium GNU/Linux .tar.gz from the owner's Toon Boom account (fmmg.mars@gmail.com only), then run install_harmony_linux.sh"
exit 1
