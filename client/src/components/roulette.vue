<template>
  <div id="roulettecard">
    <el-card>
      <canvas id="wheel" width=504 height=504></canvas>
      <script type="application/javascript">
        function drawRouletteWheel() {
          console.log("drawing roulette wheel");
          var canvas = document.getElementById("wheel");
          if (canvas.getContext) {
            ctx = canvas.getContext("2d");
            ctx.clearRect(0,0,504,504);
            ctx.strokeStyle = "black";
            ctx.lineWidth = 2;
            ctx.fillStyle = "#abcdef";

            ctx.beginPath();
            ctx.arc(252, 252, 250, 0, Math.PI * 2, false);
            ctx.stroke();
            ctx.fill();
          }
        }
        drawRouletteWheel();
      </script>
      <img id="arrow" src="../assets/arrow-right.png">
      <el-button id="choose-button" @click="locationPicker">转</el-button>
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
  margin: auto;
  display: block;
  transition: all ease 5s;
}
#arrow{
  position: absolute;
  left: 580px;
  top: 40%;
  z-index: 1;
}
#entries{
  max-height: 200px;
  padding: 0 0 10px 0;
  text-align: center;
}
#choose-button{
  position: relative;
  width: 10%;
  height: 40px;
  text-align: center;
  margin: 10px auto;
  display: block;
  padding: 0px;
  z-index: 1;
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
      spinTimeout: null,
    };
  },
  methods: {
    locationPicker() {
      this.locationNames = this.list.split(/, | |，|\n/);
      const chosenNumber = Math.floor(Math.random() * this.locationNames.length);
      this.chosenName = this.locationNames[chosenNumber];

      this.drawWheel();

      const x = 1024;
      const y = 9999;
      const deg = Math.floor(Math.random() * (x - y)) + y;
      document.getElementById('wheel').style.transform = `rotate(${deg}deg)`;
    },
    drawWheel() {
      const colors = ['#abcdef', '#d5e8ff', '#ffffff'];
      const canvas = document.getElementById('wheel');

      if (canvas.getContext) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, 504, 504);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        let angle = 0;
        const arc = ((Math.PI * 2) / this.locationNames.length);

        if (this.locationNames.length < 13) ctx.font = '50px sans-serif';
        else ctx.font = '25px sans-serif';

        for (let i = 0; i < this.locationNames.length; i += 1) {
          angle = i * arc;
          ctx.fillStyle = colors[i % 3];
          if (i === this.locationNames.length - 1 && i % 3 === 0) ctx.fillStyle = '#d5e8ff';

          ctx.beginPath();
          ctx.arc(252, 252, 250, angle, angle + arc, false);
          ctx.stroke();
          if (this.locationNames.length !== 1) ctx.arc(252, 252, 0, angle + arc, 0, false);
          ctx.fill();
          if (i === this.locationNames.length - 1) ctx.lineWidth = 1;
          ctx.stroke();

          ctx.save();
          ctx.shadowOffsetX = -1;
          ctx.shadowOffsetY = -1;
          ctx.shadowBlur = 0;
          ctx.shadowColor = 'rgb(220,220,220)';
          ctx.fillStyle = 'black';
          ctx.translate(250 + Math.cos(angle + arc / 2) * 160,
            250 + Math.sin(angle + arc / 2) * 160);
          ctx.rotate(angle + arc / 2 + Math.PI);
          const text = this.locationNames[i];
          ctx.fillText(text, -ctx.measureText(text).width / 2, 0);
          ctx.restore();
        }
      }
    },
  },
};
</script>
