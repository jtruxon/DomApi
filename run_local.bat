setlocal

    @echo off
    rem docker run -it --rm litmos-etl:latest /bin/ash
    rem docker build --rm -f "Dockerfile" -t etl:latest .

    SET TAG=domapi:latest
    if "%~1"=="" (
        docker run -it -p 8080:8080 "%TAG%"
    ) else (
        docker run -it -p 8080:8080 "%TAG%" "%~1"
    )

endlocal