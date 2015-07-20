#!/bin/bash

echo "yes" | ./manage.py collectstatic

echo "no" | ./manage.py syncdb

./manage.py migrate

./manage.py loadfixtures

./manage.py load_metadata_fixtures

python manage.py runserver 0.0.0.0:${APP_PORT}
