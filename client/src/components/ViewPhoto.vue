<template>
  <el-container style="margin-top: -7px">
  <div>
    <el-container style="margin-bottom: 4px">
    <el-button
      style="width: 50px;margin-right: 30px;"
      icon="el-icon-back"
      @click="BackToImageWall" circle
    type="primary"></el-button>
    <h1 >{{this.$props.info.caption}}</h1>
    </el-container>
    <el-container>
 <el-aside width="900px">
   <el-card :body-style="{ padding: '10px' }" shadow="hover">
     <el-image
      :src="info.src"
      :preview-src-list="[info.src]"
      :fit="fit">
    </el-image>
   </el-card>
 </el-aside>
      <el-container>

      <el-main>
        <div>
          <el-card >
            <el-container>
         <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                 style=""  :size="50"></el-avatar>
        <h3 style="margin-top: 12px;margin-left: 5px">
          {{info.username}}
        </h3>
            </el-container>
        <span style="margin-left: 5px">{{info.date_created}}</span>
           </el-card>
        </div>
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
