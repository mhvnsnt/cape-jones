# Set up on your IDE the following arguments to run from the scripts folder:
# "CompilerBin", meaning the bin folder of your compiler (Example: C:\Qt\5.15.2\mingw81_64\bin)
# This is for default GCC/MSVC and not for cmake.

param(
    [Parameter()]
    [String]$CompilerBin
)

Set-Location ..
$AEFolder = Get-Location
Set-Location $AEFolder"\src"
$AESauce = Get-Location
Invoke-Expression $CompilerBin"\windeployqt.exe --dir .\AnimeEffects-Windows "'"'$AESauce'\AnimeEffects.exe"'
Copy-Item -Path ".\data" -Destination ".\AnimeEffects-Windows\" -recurse -Force
Copy-Item ".\AnimeEffects.exe" ".\AnimeEffects-Windows\"
Write-Output Done