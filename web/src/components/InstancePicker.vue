<template>
  <v-stage ref="stage" :config="confStage">
    <v-layer ref="layer">
      <v-circle :config="confCircle"></v-circle>
    </v-layer>
  </v-stage>
</template>

<script>
export default {
  name: 'InstancePicker',
  data: function () {
    return {
      dots: [],
      confStage: {
        width: 1024,
        height: 768
      },
      confCircle: {
        x: 100,
        y: 100,
        radius: 70,
        fill: "red",
        stroke: "black",
        strokeWidth: 4
      },
      confPath:{
        sceneFunc: function(context) {
          context.beginPath();
          context.moveTo(20, 50);
          context.lineTo(220, 80);
          context.quadraticCurveTo(150, 100, 260, 170);
          context.closePath();

          // special Konva.js method
          context.fillStrokeShape(this);
        },
        fill: '#00D2FF',
        stroke: 'black',
        strokeWidth: 4
      }
    }
  },
  methods: {
  },
  components: {
  }

}

</script>

 <style scoped>

</style>
