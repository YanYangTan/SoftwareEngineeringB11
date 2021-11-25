<template>
  <div id="app">
<el-container style="height: 800px; border: 1px solid #eee">
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-user"></i>用户</template>
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
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>

  <el-container>

    <el-main>
      <Calender v-if="this.$data.index==='Calender'"></Calender>
      <GroupList v-if="this.$data.index==='GroupList'"></GroupList>
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
  },
  created() {
    this.getMessage();
  },
};
</script>
