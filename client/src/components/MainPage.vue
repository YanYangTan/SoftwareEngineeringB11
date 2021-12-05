<template>
  <div id="main-page" style="height: 100%;">
<el-container style="height: 100%; border: 1px solid #eee"> <!-- fix here -->
  <el-aside width="200x" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-user"></i>{{this.$route.params.username}}</template>
        <el-menu-item-group>
          <el-menu-item index="2-1">个人信息</el-menu-item>
          <el-menu-item index="2-2" @click="SignIn"><el-button type="text" style="color: crimson" @click="SignIn">退出登录</el-button></el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-menu"></i>归雁</template>
        <el-menu-item-group>
          <el-menu-item index="1-1" @click="TurnToGroupList">群组管理</el-menu-item>
          <el-menu-item index="1-2" @click="TurnToCalender">日历管理</el-menu-item>
          <el-menu-item index="1-3" >聚会管理</el-menu-item>
          <el-menu-item index="1-4" @click="TurnToImageWall">照片墙</el-menu-item>
          <el-menu-item index="1-5" @click="TurnToRoulette">随机轮盘</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>

  <el-container>
    <div class="mainapp">
<!--      <Calender v-if="this.$data.index==='Calender'"></Calender>-->
      <iframe id="calendar" src="/Calender" v-if="this.$data.index==='Calender'"></iframe>
        <el-main>
          <GroupList @groupPage='groupInfo' v-if="this.$data.index==='GroupList' "></GroupList>
          <GroupPage @BacktoGroupList='BackToGroupList' v-if="this.$data.index==='GroupPage'" :info="this.$data.currentgroup"></GroupPage>
          <ImageWall v-if="this.$data.index==='ImageWall'" :info="this.$data.currentgroup"></ImageWall>
          <Roulette v-if="this.$data.index==='Roulette'"></Roulette>
        </el-main>
    </div>
  </el-container>
</el-container>

<!--    <GroupList></GroupList>-->
</div>

</template>

<script>
import axios from 'axios';
import RegisterPage from './register.vue';
import GroupList from './GroupList.vue';
import Calender from './Calender.vue';
import GroupPage from './GroupPage.vue';
import ImageWall from './ImageWall.vue';
import Roulette from './roulette.vue';

export default {
  name: 'MainPage',
  // props: {
  //   // eslint-disable-next-line vue/require-prop-type-constructor
  //   userid: {
  //     type: Number,
  //     default: 1234,
  //   },
  // },
  components: {
    ImageWall,
    // eslint-disable-next-line vue/no-unused-components
    RegisterPage,
    // eslint-disable-next-line vue/no-unused-components
    Calender,
    // eslint-disable-next-line vue/no-unused-components
    GroupList,
    GroupPage,
    // eslint-disable-next-line vue/no-unused-components
    Roulette,
  },
  data() {
    return {
      // userid: '',
      msg: '',
      index: 'GroupList',
      currentgroup: {},
    };
  },
  methods: {
    groupInfo(ev) {
      this.currentgroup = ev;
      this.$data.index = 'GroupPage';
      console.log(this.currentgroup);
    },
    BackToGroupList() {
      this.$data.index = 'GroupList';
    },
    TurnToImageWall() {
      this.index = 'ImageWall';
    },
    getMessage() {
      const path = '/api/success';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    SignIn() {
      this.$router.push('/');
    },
    TurnToGroupList() {
      this.$data.index = 'GroupList';
    },
    TurnToCalender() {
      this.$data.index = 'Calender';
    },
    TurnToRoulette() {
      this.$data.index = 'Roulette';
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
<style>
#main-page{
  background: #d5e8ff;
}
.mainapp{
  width: 100%;
}
.el-main{
  height:100%;
}
#calendar{
  height: 100%;
  width: 100%;
  position: relative;
  border: none;
}
</style>
