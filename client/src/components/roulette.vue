<template>
  <div>
    <el-card>
      <el-header>
        <p>{{chosenName}}</p>
      </el-header>
        <el-input placeholder="Please input" v-model="list"></el-input>
      <el-button @click="locationPicker">Choose</el-button>
    </el-card>
  </div>
</template>

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
