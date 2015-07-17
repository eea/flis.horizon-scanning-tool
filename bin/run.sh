#!/bin/bash

django-admin collectstatic

./manage.py syncdb

./manage.py migrate

./manage.py loadfixtures
./manage.py load_metadata_fixtures

./manage.py runserver