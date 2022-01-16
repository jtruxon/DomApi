setlocal

    @echo off

    SET TAG=domapi:latest
    if "%~1"=="" (
        docker run -it --env-file .env -p 8080:8080 "%TAG%"
    ) else (
        docker run -it --env-file .env -p 8080:8080 "%TAG%" "%~1"
    )

endlocal