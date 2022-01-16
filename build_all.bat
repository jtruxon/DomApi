cls
if "%1"=="" (
    echo ERROR: Missing "DOM_API_APIVERSION" commandline arg
    echo    sample usage: %~nx0 1.5.0
    exit /B 1
)
set DOM_API_APIVERSION=%1
setx DOM_API_APIVERSION %DOM_API_APIVERSION%
python update_version.py %DOM_API_APIVERSION%
call build_dist.bat
call build.bat

