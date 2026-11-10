#!/usr/bin/env bash
# Please set this up to be run from the scripts folder #
# You need make to use of this script #

cd ..
AESource=$(pwd)
cd "$AESource/src" || echo Failed
make clean
del "$AESource/data"
del "$AESource/tools"
del "$AESource/AnimeEffects"
echo Done
