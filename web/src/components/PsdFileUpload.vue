<template>
  <div class="drag container bg-light">
    <div class="p-4">
      <div class="form-group">
        <label for="work-name">Work Name</label>
        <input type="text" id="work-name" class="form-control" v-model="info.work.title" placeholder="원피스">
      </div>
      <div class="form-group">
        <label for="work-detail">Work Detail</label>
        <textarea id="work-detail" class="form-control" v-model="info.work.detail" rows="5" placeholder="1997년 7월 22일에 연재를 시작한 오다 에이치로의 능력자 배틀 소년만화....">
        </textarea>
      </div>
      <div class="form-group">
        <label for="episode-name">Episode Name</label>
        <input type="text" id="episode-name" class="form-control" v-model="info.episode.title" placeholder="43화">
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
          post-action="api/uploads/"
          :headers="{'X-CSRFToken': this.csrfTk }"
          :data="{ 'work_title': info.work.title, 'work_detail': info.work.detail, 'episode': info.episode.title }"
          :multiple="true"
          :drop="true"
          :drop-directory="true"
          name="datafile"
          v-model="files"
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
        work: {
          title: '',
          detail: ''
        },
        episode: {
          title: ''
        },
      },
    }
  },
  method: {
  },
}
</script>

<style scoped>
.drag .btn {
  margin: 0.5rem;
}

/*

.drag .drop-active {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  position: fixed;
  z-index: 9999;
  opacity: .6;
  text-align: center;
  background: #000;
}

.drag .drop-active h3 {
  margin: -.5em 0 0;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
  font-size: 40px;
  color: #fff;
  padding: 0;
}
*/
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
