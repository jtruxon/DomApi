twine check dist/* 
twine upload dist/* -u jtruxon -p %PYPI_PW%

rem twine upload --repository-url https://test.pypi.org/legacy/ dist/*
