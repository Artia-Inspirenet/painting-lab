Changed for public service ***webapp***, artia app is deprecated.

## Possible bash commmand

`$ bash run.sh`: Same as `python manage.py runserver`

`$ bash run.sh install`: Install PyPI specified in **requirements.txt**

`$ bash run.sh install $VIRTUALENV_NAME`: Make virtualenv named *VIRTUALENV_NAME* automatically, and install PyPI specified in requirements.txt like above. Require **virtualenvwrapper**

`$ bash run.sh clean`: Remove SQL query made by command *makemigrations* and DB file if exists.

## requirement

Check out `requirements.txt`
