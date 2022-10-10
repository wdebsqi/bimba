FROM python:3.10-slim

WORKDIR /bimba

EXPOSE 5000

COPY ./db /bimba/src/db
COPY ./file_parser /bimba/src/file_parser

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip3 install -r /bimba/src/file_parser/requirements.txt

ENTRYPOINT ["python3", "-m", "src.file_parser.app"]
