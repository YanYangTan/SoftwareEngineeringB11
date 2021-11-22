<template>
  <div id="app">
<el-container style="height: 800px; border: 1px solid #eee">
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-menu"></i>导航</template>
        <el-menu-item-group>
          <el-menu-item index="1-1">群组管理</el-menu-item>
          <el-menu-item index="1-2">动态</el-menu-item>
          <el-menu-item index="1-2">家谱管理</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>

  <el-container>
    <el-header style="text-align: right; font-size: 12px">
      <el-dropdown>
        <i class="el-icon-setting" style="margin-right: 15px"></i>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>个人信息</el-dropdown-item>
          <el-dropdown-item><el-button type="text" style="color: crimson" @click="SignIn">退出登录</el-button></el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <span>白</span>
    </el-header>

    <el-main>
        <label>{{this.$route.params.userid}}</label>
          <GroupList

          ></GroupList>
    </el-main>
  </el-container>
</el-container>
</div>
</template>

<script>
import axios from 'axios';
import RegisterPage from './register.vue';
import GroupList from './GroupList.vue';

export default {
  name: 'Success',
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
    GroupList,
  },
  data() {
    return {
      // userid: '',
      msg: '',
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
  },
  created() {
    this.getMessage();
  },
};
</script>
