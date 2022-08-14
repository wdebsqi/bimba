FROM ubuntu:22.04

ENV NEO4J_URL="neo4j+s://04ad133b.databases.neo4j.io" NEO4J_USERNAME="neo4j" NEO4J_PASSWORD="c6mGHTylDdTR_bvyt5uPzCTRO6EqyUQauM8rvs9xWX4"
WORKDIR /bimba

COPY . .

EXPOSE 5001

RUN apt-get update \ 
    && apt-get install --no-install-recommends -y python3 python3-pip \
    && pip3 install -r requirements.txt

ENTRYPOINT ["python3", "run.py"]