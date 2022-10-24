# python better than python-apline image
# cuz it's make many bugs

###########
# BUILDER #
###########

FROM python:3.9 as builder

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install netcat

RUN apt-get -y install add postgresql-dev gcc python3-dev musl-dev nginx libpq-dev postgresql-client

COPY . /usr/src/app/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r /usr/src/app/requirements.txt

#########
# FINAL #
#########

FROM python:3.9

# create directory for the user
RUN mkdir -p /home/app

# create the appuser user in appuser group
# RUN addgroup -S app && adduser -S app -G app
ARG user=app
ARG group=app
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}

# create the appropriate directories
ENV DJANGO_SETTINGS_MODULE=backend_sl.settings.production
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get -y install netcat gettext nano

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R ${user}:${group} $HOME

RUN ["chmod", "+x", "/home/app/web/entrypoint.prod.sh"]