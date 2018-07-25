#!/bin/bash

# Make isolated python-virtualenv things if you wnat.
if [ $1 == "clean" ]
  then
    rm db.sqlite3
    find artia/migrations/. ! -name '__init__.py' -exec rm {} \;
    exit 1
fi

# virtualenvwrapper is reqired
if [ $# != 0 ]
  then
    . `which virtualenvwrapper.sh`
    mkvirtualenv $1
fi

# Install Pypi required
pip install --user -r requirement.txt

# Make project's DB
python manage.py migrate

# Make app's DB-making python script - now app is artia
python manage.py makemigrations

# Apply script just made. This will add table for artia's model
python manage.py migrate

# Make superuser for web-tool
pass = `cat superuserpass.txt`
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', '$pass')" | python manage.py shell

# Run server
python manage.py runserver


