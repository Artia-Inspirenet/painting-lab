<template>
  <v-stage class="container" ref="stage" :config="confStage">
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
  </v-stage>
</template>

<script>
export default {
  name: 'stage',
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
  mounted: function () {
  }

}

</script>

<style scoped>

</style>
