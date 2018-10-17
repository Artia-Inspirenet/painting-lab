# Ref.

- [Vue.js](https://kr.vuejs.org/v2/guide/index.html) with [Webpack](https://webpack.js.org/concepts/)
- [Vue CLI 3](https://cli.vuejs.org/)
- From node package: [vue-upload-component](https://lian-yue.github.io/vue-upload-component/#/en/documents), [vue-konva](http://rafaelescala.com/vue-konva-doc/), [Konva: docs](https://konvajs.github.io/docs/), [axios](https://github.com/axios/axios)
- Furthermore - not applied yet: [Vuex](https://vuex.vuejs.org/kr/), [vue-router](https://router.vuejs.org/kr/)

## Endpoints

### Home

`/`

### PSDFile Upload

`/psdfile/`

### Keypoints and Contour

`/keypoints/`

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
