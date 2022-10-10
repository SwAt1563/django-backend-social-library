FROM python:3.8-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip --no-cache-dir

# this will copy our files in /app in docker
# so after this we will access files from the /app not
# the originl files
COPY . .

RUN pip3 install -r ./requirements.txt