#!/bin/bash

python /code/home_finances/manage.py collectstatic -c --noinput
python /code/home_finances/manage.py migrate

exec "$@"