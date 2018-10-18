<template>
  <div class="container bg-light drag">
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
          :headers="{'X-CSRFToken': this.csrfTk }"
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
  </div>
</template>

<script>
import FileUpload from 'vue-upload-component'
//import axios from 'axios'


export default {
  name: 'PsdFileUpload',
  props: {
    csrfTk: String,
  },
  components: {
    FileUpload,
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
      },
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
  beforeMount: function () {
  },
}
</script>

<style scoped>
.drag .btn {
  margin: 0.5rem;
}
div div.drop-zone {
  width: 100%;
  height: 100px;
  border: 1px #ababab dashed;
  margin: 50px auto;
}

div.drop-zone p {
  text-align: center;
  line-height: 100px;
  margin: 0;
  padding: 0;
}

.drag {
  border: 1px #ababab dashed;
}

</style>
