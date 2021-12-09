<template>
  <div id="roulettecard">
    <el-card>
      <div id="chosen">
        <p>{{chosenName}}ᅠ</p>
      </div>
        <el-input id="entries" placeholder="Please input" v-model="list"></el-input>
      <el-button id="choose-button" @click="locationPicker">Choose</el-button>
    </el-card>
  </div>
</template>

<style>
#body{
  -ms-overflow-style: none;
  scrollbar-width: none;
}
#roulettecard{
  height: 90%;
}
.el-card{
  height:100%;
}
#chosen{
  height: 100% !important;
  font-size: 100px;
  text-align: center;
  padding: 100px 0 100px 0;
}
#entries{
  height: 200px !important;
  padding: 0 0 10px 0;
  text-align: center;
}
#choose-button{
  width: 100%;
}
</style>

<script>

export default {
  name: 'roulette',
  data() {
    return {
      list: '',
      locationNames: '',
      chosenName: '',
    };
  },
  methods: {
    locationPicker() {
      this.locationNames = this.list.split(/,| |，|\n/);
      const chosenNumber = Math.floor(Math.random() * this.locationNames.length);
      this.chosenName = this.locationNames[chosenNumber];
    },
  },
};
</script>
