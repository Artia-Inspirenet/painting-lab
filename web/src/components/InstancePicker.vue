<template>
  <v-stage ref="stage" :config="confStage">
    <v-layer ref="layer">
      <v-line :config="confLine"></v-line>
    </v-layer>
  </v-stage>
</template>

<script>
export default {
  name: 'InstancePicker',
  data: function () {
      let scale =  Math.random();
    return {
      confStage: {
        width: 1024,
        height: 768
      },
      confStar: {
        x: Math.random() * 1024,
        y: Math.random() * 768,
        numPoints: 5,
        innerRadius: 30,
        outerRadius: 50,
        fill: '#89b717',
        opacity: 0.8,
        draggable: true,
        scale: {
          x : scale*5,
          y : scale*10
        },
        rotation: Math.random() * 180,
        shadowColor: 'black',
        shadowBlur: 10,
        shadowOffset: {
          x : 5,
          y : 5
        },
        shadowOpacity: 0.6,
        // custom attribute
        startScale: scale
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

  },
  components: {
  },
  computed: {
  }

}

</script>

<style scoped>

</style>
