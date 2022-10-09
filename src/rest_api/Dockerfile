FROM python:3.10-slim

WORKDIR /bimba

EXPOSE 5001

COPY ./db /bimba/src/db
COPY ./rest_api /bimba/src/rest_api

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip3 install -r /bimba/src/rest_api/requirements.txt

ENTRYPOINT ["python3", "-m", "src.rest_api.app"]