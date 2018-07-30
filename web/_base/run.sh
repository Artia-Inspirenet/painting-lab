#!/bin/bash
bd=$(tput bold)
nm=$(tput sgr0)
# Make isolated python-virtualenv things if you wnat.
function clean () {
    echo "${bd}### Cleaning all these stuff including DB${nm}"
    rm db.sqlite3
    find artia/migrations/. ! -name '__init__.py' -exec rm {} \;
}

function mkvir () {

    # virtualenvwrapper is reqired
    if [ $2 != "" ]; then
        echo "${bd}### Make new virtualenv called $2${nm}"
        . `which virtualenvwrapper.sh`
        mkvirtualenv $2 -p python3
    else
        echo "${bd}### No virtualenv created. If you want to make one, just type name like below${nm}"
        echo "${bd}### $ bash run.sh install web-tool${nm}"
    fi

}

function setenv () {

    echo "${bd}### Install required python packages${nm}"
    pip3 install -r requirement.txt

    echo "${bd}### Basic default project's DB migrations${nm}"
    python3 manage.py migrate

    echo "${bd}### Make app's DB-making python script - now app is artia${nm}"
    python3 manage.py makemigrations

    echo "${bd}### Apply script just made. This will add table for artia's model${nm}"
    python3 manage.py migrate

}

function setpswd () {

    PASS=`cat superuserpass.txt`
    echo "${bd}### Make superuser for web-tool: Go http://localhost:8000/admin/${nm}"
    echo "${bd}### ID: admin${nm}"
    echo "${bd}### PW: $PASS${nm}"
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', '$PASS')" | python3 manage.py shell

}

if [ $1 == "clean" ]; then
    clean
    exit 1

elif [ $1 == "install" ]; then

    clean
    mkvir
    setenv
    setpswd

fi

# Run dev-server
python3 manage.py runserver


