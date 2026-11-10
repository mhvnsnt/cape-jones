# Please setup this to run from the scripts folder #
# This script will help to generate Makefiles for intellisense #
# For CLion you need to right click and load each makefile, in theory you only need to #
# do this once, since it should auto-reload makefiles when they change #

# Your mileage may vary #

# You may setup your qmake path here if you don't have it on your PATH, you then need only
# remove the comment character and add "$" to each qmake thereafter

# $qmake = ""

Set-Location ..
$AEFolder = Get-Location
Set-Location $AEFolder"\src"
$AESource = Get-Location
Set-Location $AESource"\cmnd"
qmake
Set-Location $AESource"\core"
qmake
Set-Location $AESource"\ctrl"
qmake
Set-Location $AESource"\gl"
qmake
Set-Location $AESource"\gui"
qmake
Set-Location $AESource"\img"
qmake
Set-Location $AESource"\thr"
qmake
Set-Location $AESource"\util"
qmake
Write-Output Done