<template>
  <v-stage ref="stage" :config="confStage">
    <v-layer ref="layer">
      <v-line :config="confLine"></v-line>
      <v-image :config="confbgImage"></v-image>
    </v-layer>
  </v-stage>
</template>

<script>
export default {
  name: 'InstancePicker',
  data: function () {
    return {
      cutUrl : '',
      cutImg: null,
      keyPoints: [],
      confStage: {
        width: 1024,
        height: 768
      },
      confLine:{
        points: [23, 20, 23, 160, 70, 93, 150, 109, 290, 139, 270, 93],
        fill: '#00D2FF',
        stroke: 'black',
        strokeWidth: 5,
        closed : true
      },
    }
  },
  methods: {
    initCutUrl: function () {
      this.$http.get("/keypoints/")
        .then((response) => {
          this.cutUrl = response.data.cutimg_url;
          this.keyPoints = response.data.keypoints;
          this.cutImg.src = this.cutUrl
        })
    },
  },
  created: function () {
    this.initCutUrl();
  },
  components: {
  },
  computed: {
    confbgImage: function () {
      this.cutImg = new Image();
      this.cutImg.src = this.cutUrl;
      return {
        x: 50,
        y: 50,
        image: this.cutImg,
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
