if "%DOM_API_APIVERSION%"=="" (
    echo ERROR: Missing "DOM_API_APIVERSION" environment variable
    exit /B 1
)
SET PYPI_PW=%1
call push_latest.bat 
call push_twine.bat