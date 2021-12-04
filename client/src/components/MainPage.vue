<template>
  <div id="app">
<el-container style="height: 100%; border: 10px solid #eee"> <!-- fix here -->
  <el-aside width="200x" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-user"></i>{{this.$route.params.username}}</template>
        <el-menu-item-group>
          <el-menu-item index="2-1">个人信息</el-menu-item>
          <el-menu-item index="2-2"><el-button type="text" style="color: crimson" @click="SignIn">退出登录</el-button></el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-menu"></i>导航</template>
        <el-menu-item-group>
          <el-menu-item index="1-1"><el-button type="text" style="color: black" @click="TurnToGroupList">群组管理</el-button></el-menu-item>
          <el-menu-item index="1-2">动态管理</el-menu-item>
          <el-menu-item index="1-3">家谱管理</el-menu-item>
          <el-menu-item index="1-4"><el-button type="text" style="color: black" @click="TurnToCalender">日历管理</el-button></el-menu-item>
          <el-menu-item index="1-5"><elbutton type="text" style="color: black" @click="TurnToRoulette">Roulette</elbutton></el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>

  <el-container>

    <el-main>
<!--      <Calender v-if="this.$data.index==='Calender'"></Calender>-->
      <iframe src="/Calender" v-if="this.$data.index==='Calender'"
              style="height: 100%;width: 100%;position: relative;margin-top: -20px;margin-left: -20px;"></iframe>
      <GroupList v-if="this.$data.index==='GroupList'"></GroupList>
      <Roulette v-if="this.$data.index==='Roulette'"></Roulette>
    </el-main>
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
    // eslint-disable-next-line vue/no-unused-components
    RegisterPage,
    // eslint-disable-next-line vue/no-unused-components
    Calender,
    // eslint-disable-next-line vue/no-unused-components
    GroupList,
    // eslint-disable-next-line vue/no-unused-components
    Roulette,
  },
  data() {
    return {
      // userid: '',
      msg: '',
      index: 'Calender',
    };
  },
  methods: {
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
