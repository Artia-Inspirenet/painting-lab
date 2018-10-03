Changed for public service ***webapp***, artia app is deprecated.

# django - backend

## Possible bash commmand

`$ bash run.sh`: Same as `python manage.py runserver`

`$ bash run.sh install`: Install PyPI specified in **requirements.txt**

`$ bash run.sh install $VIRTUALENV_NAME`: Make virtualenv named *VIRTUALENV_NAME* automatically, and install PyPI specified in requirements.txt like above. Require **virtualenvwrapper**

`$ bash run.sh clean`: Remove SQL query made by command *makemigrations* and DB file if exists.

`$ bash run.sh npmi`: Install npm library for developing vuejs

## requirement

Check out `requirements.txt`

# Vue.js - frontend

Vue.js based webpack auto-generated README.md

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
