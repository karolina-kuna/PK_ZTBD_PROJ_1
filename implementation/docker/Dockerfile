FROM python:3.9-slim-buster

ENV GUNICORN_LOG_LEVEL="info"

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc python-dev libpq-dev musl-dev
#RUN apt-get install -y libpq-dev postgresql-client
#RUN apt-get install -y wget \
#    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
#    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
#    && rm dockerize-linux-amd64-v0.6.1.tar.gz

COPY . ./app/
COPY ./requirements.txt ./

WORKDIR app

RUN pip install -U pip
RUN pip install -r ./requirements.txt

EXPOSE 5000

#ENTRYPOINT ["./docker/entrypoints/entrypoint.sh"]