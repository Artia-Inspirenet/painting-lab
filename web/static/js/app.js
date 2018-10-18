Vue.config.productionTip = false
Vue.prototype.$http = axios

Vue.filter('formatSize', function (size) {
  if (size > 1024 * 1024 * 1024 * 1024) {
    return (size / 1024 / 1024 / 1024 / 1024).toFixed(2) + ' TB'
  } else if (size > 1024 * 1024 * 1024) {
    return (size / 1024 / 1024 / 1024).toFixed(2) + ' GB'
  } else if (size > 1024 * 1024) {
    return (size / 1024 / 1024).toFixed(2) + ' MB'
  } else if (size > 1024) {
    return (size / 1024).toFixed(2) + ' KB'
  }
  return size.toString() + ' B'
})

const store = new Vuex.Store({
  state: {
  },
  mutations: {
  }
})

Vue.component('file-upload', VueUploadComponent)

var PsdFileUpload = {
  template: `
  <div id="psd-file-upload" class="container bg-light drag">
    <div class="p-4">
      <div class="form-group">
        <label for="author-name">Author Name</label>
        <input type="text" id="author-name" class="form-control" v-model="info.author.name" placeholder="조석">
      </div>
      <div class="form-group">
        <label for="work-name">Work Name</label>
        <input type="text" id="work-name" class="form-control" v-model="info.work.title" placeholder="마음의 소리">
      </div>
      <div class="form-group">
        <label for="episode-name">Episode Name</label>
        <input type="text" id="episode-name" class="form-control" v-model="info.episode.title" placeholder="643화">
      </div>
    </div>
    <div class="upload">
      <ul class="list-unstyled p-5" v-if="files.length">
        <li v-for="file in files" :key="file.id">
          <span>{{file.name}}</span> -
          <span>{{file.size | formatSize}}</span> -
          <span v-if="file.error">{{file.error}}</span>
          <span v-else-if="file.success">success</span>
          <span v-else-if="file.active">active</span>
          <span v-else-if="file.active">active</span>
          <span v-else></span>
        </li>
      </ul>
      <ul v-else>
        <div class="text-center p-5"
          v-if="$refs.upload && $refs.upload.dropActive">
          <h4>Ya! Drop them!</h4>
        </div>
        <div class="text-center p-5"
          v-else>
          <h4>Drag files here!</h4>
        </div>
      </ul>


      <div class="btn">
        <file-upload
          class="btn btn-primary"
          post-action="psdfile/"
          :headers="{ 'X-CSRFToken' : this.csrfTk }"
          :data="{ author: info.author.name, work: info.work.title, episode: info.episode.title }"
          :multiple="true"
          :drop="true"
          :drop-directory="true"
          name="psdfile"
          v-model="files"
          @input-filter="psdFilter"
          ref="upload">
          <i class="fa fa-plus"></i>
          Select files
        </file-upload>
        <button
          class="btn btn-success"
          v-if="!$refs.upload || !$refs.upload.active"
          @click.prevent="$refs.upload.active = true">
          <i class="fa fa-arrow-up" aria-hidden="true"></i>
          Start Upload
        </button>
        <button
          class="btn btn-danger"
          v-else @click.prevent="$refs.upload.active = false">
          <i class="fa fa-stop" aria-hidden="true"></i>
          Stop Upload
        </button>
      </div>
    </div>
  </div>`,
  props: {
    csrfTk: String,
  },
  data: function () {
    return {
      files: [],
      info: {
        author: {
          name: ''
        },
        work: {
          title: '',
        },
        episode: {
          title: '',
        },
      }
    }
  },
  methods: {
    psdFilter: function (newFile, oldFile, prevent) {
      if (!/\.(psd)$/i.test(newFile.name)) {
        return prevent()
      }
    },
    getResponse: function (newFile, oldFile) {
      if (newFile && oldFile && !newFile.active && oldFile.active) {
        // Get response data
        console.log('response', newFile.response)
        if (newFile.xhr) {
          //  Get the response status code
          console.log('status', newFile.xhr.status)
        }
      }
    },
  },
}

var InstancePicker = {
  template: `
  <v-stage id="instance-picker" class="container" ref="stage" :config="confStage">
    <v-layer ref="cutimg">
      <v-image :config="confbgImage"></v-image>
    </v-layer>
    <v-layer ref="keypoints">
      <v-circle
        v-for="point in confKeyPoints"
        @mousemove="handleMouseOver"
        @mouseout="handleMouseOut"
        :config="{ x: point.x,
                   y: point.y,
                   radius: 5,
                   fill: 'rgb(0,155,255,0.5)',
                   stroke: 'black',
                   strokeWidth: 2}"
        ></v-circle>
      <v-text ref="msgtext" :config="msgText"></v-text>
    </v-layer>
  </v-stage>`,
  data: function () {
    return {
      cutUrl : '',
      confStage: {
        width: 1024,
        height: 768
      },
      confKeyPoints: [],
      msgText: {
        x: 10,
        y: 10,
        fontFamily: 'Calibri',
        fontSize: 24,
        text: '',
        fill: 'black'
      }
    }
  },
  methods: {
    initCutUrl: function () {
      this.$http.get("/keypoints/")
        .then((response) => {
          this.cutUrl = response.data.cutimg_url;
          this.confKeyPoints = response.data.keypoints;
        })
    },
    writeMessage: function (message) {
      this.$refs.msgtext.getStage().setText(message);
      this.$refs.keypoints.getStage().draw();
    },
    handleMouseOver: function (vueComponent, event) {
      const mousePos = this.$refs.stage.getStage().getPointerPosition();
      const x = mousePos.x;
      const y = mousePos.y;
      this.writeMessage('x: ' + x + ', y: ' + y);
    },
    handleMouseOut: function (vueComponent, event) {
      this.writeMessage('Mouseout triangle');
    },
  },
  created: function () {
    this.initCutUrl();
  },
  components: {
  },
  computed: {
    confbgImage: function () {
      let img = new Image();
      img.src = this.cutUrl;
      return {
        x: 50,
        y: 50,
        image: img,
        width: 640,
        height: 640
      }
    }
  },
}

var csrftoken = Cookies.get('csrftoken');

var app = new Vue({
  el: '#app',
  store,
  data: {
    token: csrftoken,
  },
  components: {
    'psd-file-upload': PsdFileUpload,
    'instance-picker': InstancePicker
  },
})


