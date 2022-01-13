FROM continuumio/miniconda3

LABEL Name=domapi Version=0.0.2

EXPOSE 8080
WORKDIR /home

COPY requirements.txt ./
RUN pip install -q -r requirements.txt

COPY api ./api
COPY config ./config
COPY monitor ./monitor
COPY rest_wrapper ./rest_wrapper
COPY tests ./tests
COPY request_schema.json ./

CMD ["gunicorn", "-b 0.0.0.0:8080", "-t 600", "rest_wrapper.wrapper:flask_app"]
#CMD ["python", "-m", "rest_wrapper.wrapper"]

