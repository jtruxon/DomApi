# FROM python:3.9-slim-bullseye
FROM python:3.9-alpine

LABEL Name=domapi Version=1.1.0

WORKDIR /home

COPY requirements.txt ./
COPY dist ./dist

RUN pip install -q -r requirements.txt --no-cache-dir && \
    pip install dist/DomApi-1.1.0.tar.gz --no-cache-dir && \
    rm requirements.txt && \
    pip cache purge && \
    rm -rf dist && \
    rm -rf ~/.cache/pip

COPY run*.sh ./

EXPOSE 8080

CMD ["gunicorn", "-b 0.0.0.0:8080", "-t 600", "DomApi.rest_wrapper:flask_app"]
#CMD ["python", "-m", "DomAPI.rest_wrapper.wrapper"]

