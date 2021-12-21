<template>
  <el-container>
  <div>
    <el-button
      style="width: 50px;margin-right: 30px;"
      icon="el-icon-back"
      @click="BackToImageWall" circle
    type="primary"></el-button>
    <h1>{{this.$props.info.caption}}</h1>
    <el-container>
 <el-aside width="1000px">
   <el-card :body-style="{ padding: '10px' }" shadow="hover">

     <el-image
      style="width: 1000px; height: auto"
      :src="info.src"
      :fit="fit">
    </el-image>

   </el-card>
 </el-aside>
      <el-container>
      <el-header>{{info.date_created}}</el-header>

      <el-main>
        <h3>
          {{info.username}}
        </h3>
      </el-main>

    </el-container>
</el-container>
  </div>
  </el-container>
</template>
import axios from 'axios';

<script>
export default {
  name: 'ViewPhoto',
  data() {
    return {
      comment: '',
      fits: ['contain'],
    };
  },
  props: {
    info: {},
  },
  methods:
      {
        BackToImageWall() {
          this.$emit('BacktoImageWall');
        },
      },
  created() {
    console.log('success!');
  },
};
</script>

<style scoped>
  .el-image {
    width: 100%;
    object-fit: scale-down;
  }
</style>
