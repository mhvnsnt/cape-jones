#!/usr/bin/env bash
# Please set this up to be run from the scripts folder #
# You need gcc, make, libglib2.0-0/glib2 and qt5-default to make use of this script #

# You know the drill #

cd ..
AESource=$(pwd)
cd "$AESource/src" || echo Failed
qmake AnimeEffects.pro
make
echo Done, running...
chmod u+x ./AnimeEffects
./AnimeEffects
