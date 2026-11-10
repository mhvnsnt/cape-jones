# Set up on your IDE the following arguments to run from the scripts folder:
# "CompilerBin", meaning the bin folder of your compiler (Example: C:\Qt\5.15.2\mingw81_64\bin)
# "ToolingBin", meaning the bin folder of the tool of said compiler (Example: D:\Qt\Tools\mingw81_64\bin)
# "CompilerType", meaning the type of compiler you prefer, currently only MinGW has any real support
# "BuildType", meaning the type of build, "release" or "debug"
# "Architecture", meaning either x86 or x64 builds
# "Platform" needs to be in the Qt -spec format, win32, unix or macx for example,
# you also need to add your compiler, like g++.

param(
    [Parameter()]
    [String]$CompilerBin,
    [String]$ToolingBin,
    [String]$CompilerType = "mingw",
    [String]$BuildType = "release",
    [String]$Platform = "win32-g++"
)

Set-PSDebug -Off

$MingwCompiler = ("MinGW", "mingw", "Mingw", "MinGw")
$MSVCCompiler = ("MSVC", "msvc")
$debug = "debug"
$release = "release"

Set-Location ..
$AEFolder = Get-Location
Set-Location $AEFolder"\src"
Write-Output "Initializing compilation"
$env:Path += ";$CompilerBin;$ToolingBin"

if ($BuildType -in $debug)
{
    Write-Output "Debug spec"
    Invoke-Expression $CompilerBin'\qmake.exe -spec '$Platform' "CONFIG+=debug" "CONFIG+=qml_debug"'
}
elseif ($BuildType -in $release)
{
    Write-Output "Release spec"
    Invoke-Expression $CompilerBin'\qmake.exe -spec '$Platform' "CONFIG+=release" "CONFIG+=qml_release"'
}
else{
    Write-Output "Build type invalid or not found, defaulting to release"
}

if ($CompilerType -in $MingwCompiler){
    Write-Output "MinGW detected"
    Set-PSDebug -Trace 1
    Invoke-Expression $ToolingBin"\mingw32-make.exe -j8"
}
elseif ($CompilerType -in $MSVCCompiler){
    Write-Output "MSVC detected"
    Set-PSDebug -Trace 1
    Invoke-Expression $ToolingBin"\nmake.exe"
}

Write-Output "Compiled, running"

./AnimeEffects.exe