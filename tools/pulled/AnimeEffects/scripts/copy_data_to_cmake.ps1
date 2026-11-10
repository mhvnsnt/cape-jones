# The script can target both CLion and VSCode default CMake target folders, it must be run from the "scripts" folder.
# Default path assumed: AnimeEffects/src/cmake-build-*build-type*
Set-Location $PSScriptRoot
if (Test-Path -Path "..\src\cmake-build-debug\"){
    Copy-Item -Path "..\data" -Destination "..\src\cmake-build-debug\gui" -recurse -Force
    Write-Output "Data copied to debug folder"
}
if (Test-Path -Path "..\src\cmake-build-release\"){
    Copy-Item -Path "..\data" -Destination "..\src\cmake-build-release\gui" -recurse -Force
    Write-Output "Data copied to release folder"
}
if (Test-Path -Path "..\build\"){
    Copy-Item -Path "..\data" -Destination "..\build\gui" -recurse -Force
    Write-Output "Data copied to build folder"
}

Write-Output Done