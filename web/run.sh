#!/bin/bash
bd=$(tput bold)
nm=$(tput sgr0)

# Make isolated python-virtualenv things if you wnat.
function clean () {
    echo "${bd}### Cleaning all these stuff including sqlite DB${nm}"
    rm db.sqlite3
#    rm -rf node_modules
    find uploads/. -type f ! -name '.gitkeep' ! -name 'humanlogo.png' -exec rm {} \;
    find webapp/__pycache__/. -type f ! -name '__init__.*' -exec rm {} \;
    find webapp/migrations/. -type f ! -name '__init__.py' -exec rm {} \;
    find webapp/migrations/__pycache__/. -type f ! -name '__init__.*' -exec rm {} \;
}

function mkvir () {

    # virtualenvwrapper is reqired
    if [ "$2" != "" ]; then
        echo "${bd}### Make new virtualenv called $2${nm}"
        . `which virtualenvwrapper.sh`
        mkvirtualenv $2 -p python3
    else
        echo "${bd}### No virtualenv created. If you want to make one, just type name like below${nm}"
        echo "${bd}### $ bash run.sh install webapp${nm}"
    fi

}

function setenv () {

    echo "${bd}### Install required python packages${nm}"
    pip3 install -r requirements.txt

    echo "${bd}### Basic default project's DB migrations${nm}"
    python3 manage.py migrate

    echo "${bd}### Make app's DB-querying python script - now app is webapp${nm}"
    python3 manage.py makemigrations

    echo "${bd}### Apply script above. This will add table for webapp's model${nm}"
    python3 manage.py migrate

}

function setpswd () {

    PASS=`cat superuserpass.txt`
    echo "${bd}### Make superuser for webapp: Go http://localhost:8000/admin/${nm}"
    echo "${bd}### ID: admin${nm}"
    echo "${bd}### PW: $PASS${nm}"
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', '$PASS')" | python3 manage.py shell

}

function vueinit (){

    echo "${bd}### Install required npm_modules${nm}"
    npm install

}

if [ "$1" = "clean" ]; then
    clean
    exit 1

elif [ "$1" = "install" ]; then

    clean
    mkvir
    setenv
    setpswd

elif [ "$1" = "npmi" ]; then

    vueinit

fi

# Run dev-server
python3 manage.py runserver


