#!/bin/sh

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createadmin --username admin --email 1190777@student.birzeit --password 1

exec "$@"