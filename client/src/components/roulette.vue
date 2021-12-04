<template>
  <div>
    <el-card>
      <el-header>
        <roller text="lol"></roller>
        <p>{{chosenName}}</p>
      </el-header>
        <el-input placeholder="Please input" v-model="list"></el-input>
      <el-button @click="locationPicker">Choose</el-button>
    </el-card>
  </div>
</template>

<script>
import Roller from 'vue-roller';

export default {
  name: 'roulette',
  components: {
    Roller,
  },
  data() {
    return {
      list: '',
      locationNames: '',
      chosenName: '',
    };
  },
  methods: {
    locationPicker() {
      this.locationNames = this.list.split(',');
      const chosenNumber = Math.floor(Math.random() * this.locationNames.length);
      this.chosenName = this.locationNames[chosenNumber];
    },
  },
};
</script>
