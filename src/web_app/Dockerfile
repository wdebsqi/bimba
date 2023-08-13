FROM python:3.10-slim

WORKDIR /bimba

EXPOSE 80

COPY ./db /bimba/src/db
COPY ./web_app /bimba/src/web_app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip3 install -r /bimba/src/web_app/requirements.txt

ENTRYPOINT ["python3", "-m", "src.web_app.app"]