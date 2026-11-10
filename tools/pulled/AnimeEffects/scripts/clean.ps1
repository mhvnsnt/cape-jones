# This *only* cleans the most obtrusive files, for the time being
# "-erroraction 'silentlycontinue'" has been added since, for some reason,
# the try-catch block simply refuses to work ;w;

# Set up on your IDE the following arguments to run from the scripts folder:
# "ToolingBin", meaning the bin folder of the tool of your compiler (Example: D:\Qt\Tools\mingw81_64\bin)
# "CompilerType", meaning the type of compiler you prefer, currently only MinGW has any real support
# "Platform", meaning the one you're compiling this from

param(
    [Parameter()]
    [String]$ToolingBin,
    [String]$CompilerType = "mingw",
    [String]$Platform = "win"
)

Set-Location ..
$AEFolder = Get-Location
Set-Location $AEFolder"\src"
$AESauce = Get-Location

Set-PSDebug -Trace 1

if ("mingw" -in $CompilerType){
    Invoke-Expression $ToolingBin"\mingw32-make.exe clean"
}
elseif ("msvc" -in $CompilerType){
    Invoke-Expression $ToolingBin"\nmake.exe clean"
}
else{
    Write-Output "Compiler type is invalid"
    break
}

Set-PSDebug -Off

try { Remove-Item ".\data\" -Recurse -Confirm:$false -erroraction 'silentlycontinue'}
catch { "Cannot find the data folder, continuing..." }
finally { "Data folder deleted or not found" }

try { Remove-Item ".\tools\" -Recurse -Confirm:$false -erroraction 'silentlycontinue'}
catch [ItemNotFoundException]{ "Cannot find the tools folder, continuing..." }
finally { "Tools folder deleted or not found" }

try
{
    if ("win" -in $platform)
    {
        Remove-Item $AESauce"\AnimeEffects.exe" -Confirm:$false -erroraction 'silentlycontinue'
    }
    else
    {
        Remove-Item ".\AnimeEffects"
    }
}
catch [ItemNotFoundException]{ "Cannot find the AnimeEffects executable, ending." }
finally { "Anime Effects executable deleted or not found" }
