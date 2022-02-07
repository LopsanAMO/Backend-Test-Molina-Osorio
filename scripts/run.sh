#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py collectstatic --noinput
python manage.py migrate

ls

uwsgi --socket :9000 --workers 4 --master --enable-threads --module corner_test.wsgi:application
