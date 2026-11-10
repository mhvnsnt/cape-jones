#!/usr/bin/env bash
# Please set this up to be run from the scripts folder #
# You need qt5-default to make use of this script #

cd ..
AESource=$(pwd)
cd "$AESource/src" || echo Failed
qmake
cd "$AESource/src/cmnd" || echo Failed
qmake
cd "$AESource/src/core" || echo Failed
qmake
cd "$AESource/src/ctrl" || echo Failed
qmake
cd "$AESource/src/gl" || echo Failed
qmake
cd "$AESource/src/gui" || echo Failed
qmake
cd "$AESource/src/img" || echo Failed
qmake
cd "$AESource/src/thr" || echo Failed
qmake
cd "$AESource/src/util" || echo Failed
qmake
echo Done

