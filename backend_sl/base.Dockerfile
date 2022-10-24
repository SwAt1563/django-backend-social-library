FROM python:3.8-alpine
# alpine manger: apk

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# PYTHONDONTWRITEBYTECODE: This will remove .pyc files from our container which is a good optimization.
# PYTHONUNBUFFERED: This will buffer our output so it will look “normal” within Docker for us.

RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip --no-cache-dir

RUN apk update
RUN apk add --no-cache netcat-openbsd
RUN apk --no-cache add icu-dev gettext gettext-dev


RUN mkdir /app
WORKDIR /app

# this will copy our files in /app in docker
# so after this we will access files from the /app not
# the originl files
COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

RUN chmod +x ./entrypoint.sh
RUN touch ./logs/celery.log
RUN chmod +x /app/logs/celery.log


