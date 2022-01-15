# FROM python:3.9-slim-bullseye
FROM python:3.9-alpine

LABEL Name=domapi Version=0.1.0

WORKDIR /home

COPY requirements.txt ./
COPY dist ./dist

RUN pip install -q -r requirements.txt && \
    pip install dist/DomApi-0.1.0.tar.gz && \
    rm -rf dist && \
    rm requirements.txt

COPY run.sh ./
COPY request_schema.json ./

EXPOSE 8080

CMD ["gunicorn", "-b 0.0.0.0:8080", "-t 600", "DomApi.rest_wrapper.wrapper:flask_app"]
#CMD ["python", "-m", "DomAPI.rest_wrapper.wrapper"]

