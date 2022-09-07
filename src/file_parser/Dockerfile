FROM python:3.10-slim

WORKDIR /bimba

EXPOSE 5002

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip3 install requests pandas flask flask_sqlalchemy flask_migrate psycopg2 python-dotenv neo4j


ENTRYPOINT ["python3", "-m", "src.file_parser.app"]

COPY ./db /bimba/src/db
COPY ./file_parser /bimba/src/file_parser
