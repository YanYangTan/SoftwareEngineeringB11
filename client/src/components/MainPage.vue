<template>
  <div id="main-page" style="height: 100%;">
<el-container style="height: 100%; border: 1px solid #eee"> <!-- fix here -->
    <el-aside width="200x" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['2', '3']">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-user"></i>{{this.$route.params.username}}</template>
        <el-menu-item-group>
          <el-menu-item index="2-1" @click="TurnToProfile">个人信息</el-menu-item>
          <el-menu-item index="2-2" @click="SignIn"><el-button type="text" style="color: crimson" @click="SignIn">退出登录</el-button></el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-menu"></i>目录</template>
        <el-menu-item-group>
          <el-menu-item index="1-2" @click="TurnToGroupList">群组目录</el-menu-item>
          <el-submenu index="3">
          <template slot="title"><img src="../assets/logo.png" alt="归雁" width="30px" >{{currentgroup.group_name}}</template>
            <el-menu-item index="1-2-1" @click="TurnToGroupPage">成员管理</el-menu-item>
            <el-menu-item index="1-2-2" @click="TurnToGroupCalendar">日历管理</el-menu-item>
            <el-menu-item index="1-2-3" @click="TurnToGatherList">聚会管理</el-menu-item>
            <el-menu-item index="1-2-4" @click="TurnToImageWall">照片墙</el-menu-item>
            </el-submenu>

          <el-menu-item index="1-3" @click="TurnToUserCalendar">个人日历</el-menu-item>
          <el-menu-item index="1-4" @click="TurnToRoulette">随机转盘</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>

  <el-container>
    <div class="mainapp">
  <!--      <Calender v-if="this.$data.index==='Calender'"></Calender>-->
        <iframe id="calendar" :src=this.$data.calendarURL v-if="this.$data.index==='Calendar'"></iframe>
        <el-main>
          <Profile v-if="this.$data.index==='ProfilePage'"></Profile>
          <GroupList @groupPage='groupInfo' @defaultGroup="defaultedGroup" v-if="this.$data.index==='GroupList' "></GroupList>
          <GroupPage @BacktoGroupList='BackToGroupList' v-if="this.$data.index==='GroupPage'" :info="this.$data.currentgroup"></GroupPage>
          <ImageWall @viewPhoto='viewPhoto' v-if="this.$data.index==='ImageWall'" :info="this.$data.currentgroup"></ImageWall>
          <ViewPhoto @BacktoImageWall='BackToImageWall' v-if="this.$data.index==='ViewPhoto'" :info="this.$data.currentpic"></ViewPhoto>
          <Roulette v-if="this.$data.index==='Roulette'"></Roulette>
          <GatherList id="GatherList" :currentgroup="this.currentgroup" v-if="this.$data.index==='GatherList'"></GatherList>
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
import GatherList from './GatherList.vue';
import Profile from './ProfilePage.vue';
import ViewPhoto from './ViewPhoto.vue';

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
    GroupList,
    GroupPage,
    Roulette,
    GatherList,
    Profile,
    ViewPhoto,
  },
  data() {
    return {
      // userid: '',
      calendarURL: '',
      msg: '',
      index: 'GroupList',
      defaultgroup: false,
      currentgroup: {},
      currentpic: {},
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
    viewPhoto(dunno) {
      this.currentpic = dunno;
      this.$data.index = 'ViewPhoto';
      console.log(this.currentpic);
    },
    BackToImageWall() {
      this.$data.index = 'ImageWall';
    },
    TurnToImageWall() {
      if (this.$data.currentgroup.id === undefined) {
        this.$message({
          type: 'warning',
          message: '你不在任何群!',
        });
      } else {
        this.index = 'ImageWall';
      }
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
    TurnToGroupCalendar() {
      if (this.$data.currentgroup.id === undefined) {
        this.$message({
          type: 'warning',
          message: '你不在任何群!',
        });
      } else {
        // eslint-disable-next-line
        this.$data.calendarURL = '/Calender/1/' + this.$data.currentgroup.id;
        this.$data.index = 'Calendar';
      }
    },
    TurnToUserCalendar() {
      // eslint-disable-next-line
      this.$data.calendarURL = '/Calender/0/' + this.$route.params.userid;
      this.$data.index = 'Calendar';
    },
    TurnToRoulette() {
      this.$data.index = 'Roulette';
    },
    TurnToGroupPage() {
      if (this.$data.currentgroup.id === undefined) {
        this.$message({
          type: 'warning',
          message: '你不在任何群!',
        });
      } else {
        this.$data.index = 'GroupPage';
      }
    },
    TurnToGatherList() {
      if (this.$data.currentgroup.id === undefined) {
        this.$message({
          type: 'warning',
          message: '你不在任何群!',
        });
      } else {
        this.$data.index = 'GatherList';
      }
    },
    TurnToProfile() {
      this.$data.index = 'ProfilePage';
    },
    defaultedGroup(ev) {
      if (ev === undefined) {
        console.log('No group');
      } else if (this.defaultgroup === false) {
        this.currentgroup = ev;
        this.defaultgroup = true;
      }
    },
  },
  created() {
    this.$message({
      type: 'success',
      message: `${this.$route.params.username} ，欢迎来到归雁`,
    });
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

#GatherList{
  height: 100%;
}
</style>
