<template>
  <div id="roulettecard">
    <el-card>
      <div id="wheel">
        <div id="box" class="box">
          <div class="box1">
            <span class="span1"><b>{{locationNames[0]}}</b></span>
            <span class="span2"><b>{{locationNames[1]}}</b></span>
            <span class="span3"><b>{{locationNames[2]}}</b></span>
            <span class="span4"><b>{{locationNames[3]}}</b></span>
          </div>
          <div class="box2">
            <span class="span1"><b>{{locationNames[4]}}</b></span>
            <span class="span2"><b>{{locationNames[5]}}</b></span>
            <span class="span3"><b>{{locationNames[6]}}</b></span>
            <span class="span4"><b>{{locationNames[7]}}</b></span>
          </div>
        </div>
      </div>
      <el-button id="choose-button" @click="locationPicker">SPIN</el-button>
      <el-input id="entries" type="textarea" :autosize="{minRows:2, maxRows:9}" placeholder="Please input" v-model="list"></el-input>
    </el-card>
  </div>
</template>

<style>
#body{
  -ms-overflow-style: none;
  scrollbar-width: none;
}
#wheel{
  position: relative;
  width: 500px;
  height: 500px;
  margin: auto;
}
#entries{
  max-height: 200px;
  padding: 0 0 10px 0;
  text-align: center;
}
#wheel:before{
  position: absolute;
  content: '';
  width: 32px;
  height: 32px;
  background: url('../assets/arrow-left.png') no-repeat;
  background-size: 32px;
  right: 0;
  top: 50%;
  transform: translateY(-25%);
  z-index: 1;
}
.box{
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: 50%;
  border: 10px solid #333;
  overflow: hidden;
  transition: all ease 5s;
}

.span1{
  width: 50%;
  height: 50%;
  display: inline-block;
  position: absolute;

  clip-path: polygon(0 92%, 100% 50%, 0 8%);
  top: 120px;
  left: 0;
  background-color: #d5e8ff;
}
.span2{
  width: 50%;
  height: 50%;
  display: inline-block;
  position: absolute;

  clip-path: polygon(100% 92%, 0 50%, 100% 8%);
  top: 120px;
  right: 0;
  background-color: #ffffff;
}
.span3{
  width: 50%;
  height: 50%;
  display: inline-block;
  position: absolute;

  clip-path: polygon(50% 0%, 8% 100%, 92% 100%);
  bottom: 0;
  left: 120px;
  background-color: #a7caf5;
}
.span4{
  width: 50%;
  height: 50%;
  display: inline-block;
  position: absolute;

  clip-path: polygon(50% 100%, 92% 0, 8% 0);
  top: 0;
  left: 120px;
  background-color: #7cb4f7;
}

.box2{
  width: 100%;
  height: 100%;
  transform: rotate(-135deg);
}
span b{
  width: 65px;
  height: 65px;
  line-height: 65px;
  border-radius: 50%;
  font-size: 26px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
#choose-button{
  width: 10%;
  height: 40px;
  text-align: center;
  margin: 10px auto;
  display: block;
  padding: 0px;
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
      const x = 1024;
      const y = 9999;
      const deg = Math.floor(Math.random() * (x - y)) + y;
      document.getElementById('box').style.transform = `rotate(${deg}deg)`;

      this.locationNames = this.list.split(/,| |，|\n/);
      const chosenNumber = Math.floor(Math.random() * this.locationNames.length);
      this.chosenName = this.locationNames[chosenNumber];
    },
  },
};
</script>
