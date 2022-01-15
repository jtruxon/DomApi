# FROM python:3.9-slim-bullseye
FROM python:3.9-alpine

LABEL Name=domapi Version=0.0.2
WORKDIR /home

COPY requirements.txt ./
RUN pip install -q -r requirements.txt

COPY DomApi ./DomApi

EXPOSE 8080
# COPY api ./api
# COPY config ./config
# COPY monitor ./monitor
# COPY rest_wrapper ./rest_wrapper
# COPY tests ./tests
# COPY request_schema.json ./

CMD ["gunicorn", "-b 0.0.0.0:8080", "-t 600", "DomApi.rest_wrapper.wrapper:flask_app"]
#CMD ["python", "-m", "DomAPI.rest_wrapper.wrapper"]

