
# Vue.js - frontend

Repackaged to edit easily. Any `npm` commands are not necessary. Edit `/static/js/app.js` directly. Webpack, node.js based development server are removed. Just type `python manage.py runserver` or `bash run.sh`


## Endpoints

### Home

`/`: Just renders `templates/base.html` and does nothing else.

### PSDFile Upload

`/psdfile/`: Consumed by POST request. `psdfile` can be one or many.

**JSON Request content**
```json
{
    "author": String,
    "work": String,
    "episode": String,
    "psdfile": <binary file>,
    "psdfile": <binary file>,
    .
    .
    "psdfile": <binary file>
}
```

**JSON Response**
```json
{
    "status": "success"
}
```

### Keypoints and Contour

`/keypoints/`: Consumed by GET request. `keypoints`'s elements can be one or many.

**JSON Response**
```json
{
    "cutimg_url": String,
    "keypoints": [{ "x": Number, "y": Number },
                  { "x": Number, "y": Number },
                  .
                  .
                  { "x": Number, "y": Number }]
}
```

# django - backend

## Possible bash commmand

`$ bash run.sh`: Same as `python manage.py runserver`

`$ bash run.sh install`: Install PyPI specified in **requirements.txt**

`$ bash run.sh install $VIRTUALENV_NAME`: Make virtualenv named *VIRTUALENV_NAME* automatically, and install PyPI specified in requirements.txt like above. **virtualenvwrapper** is Required.

`$ bash run.sh clean`: Remove SQL query made by command *makemigrations* and DB file if exists.


## requirement

Check out `requirements.txt`

# Ref.

- [Vue.js](https://kr.vuejs.org/v2/guide/index.html)
- From node package: [vue-upload-component](https://lian-yue.github.io/vue-upload-component/#/en/documents), [vue-konva](http://rafaelescala.com/vue-konva-doc/), [Konva: docs](https://konvajs.github.io/docs/), [axios](https://github.com/axios/axios)
- Furthermore - applied but not used yet: [Vuex](https://vuex.vuejs.org/kr/)
