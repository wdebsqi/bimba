FROM ubuntu:22.04

WORKDIR /bimba

COPY . .

EXPOSE 5000

RUN apt-get update \ 
    && apt-get install --no-install-recommends -y python3 python3-pip \
    && pip3 install -r requirements.txt

ENTRYPOINT ["python3", "run.py"]