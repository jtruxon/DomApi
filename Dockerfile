FROM continuumio/miniconda3

LABEL Name=domapi Version=0.0.1

EXPOSE 8080
WORKDIR /home

COPY requirements.txt ./
RUN pip install -q -r requirements.txt

COPY api ./api
COPY request_schema.json ./

CMD ["gunicorn", "-b 0.0.0.0:8080", "-t 600", "api.worker:flask_app"]
#CMD ["python", "-m", "api.worker"]

