<template>
  <div>
    <el-button class="el-icon-circle-plus" type="primary" @click="createGroup"> 创建群组</el-button>
    <el-button class="el-icon-connection" type="primary" @click="joinGroup"> 加入群组</el-button>
    <div class="group-list" v-loading.fullscreen.lock="fullscreenLoading">

      <el-row :gutter="20">
        <el-col :span="3" v-for="item in grouplist" :key="item.id" style="height:200px">
          <el-card :body-style="{ padding: '0px 0px' }" >

            <div slot="header">
              <img src="../assets/logo.png" style="width:100px;height:100px;" @click="groupPage(item)" class="head_audio" />
            </div>
            <!-- here to fix text -->
<!--            <span style="font-size: 15px;">{{item.group_name}}</span>-->
            <el-button size="mini" icon="el-icon-edit-outline" style="padding: 1px 1px;" type="text"
                       class="button" @click="groupPage(item)">{{item.group_name}}</el-button>
          </el-card>
        </el-col>
      </el-row>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'app',
  data() {
    return {
      fullscreenLoading: true,
      grouplist: [],
      userid: '',
    };
  },
  methods:
    {
      // eslint-disable-next-line camelcase,no-unused-vars
      groupPage(item) {
        this.$emit('groupPage', item);
      },
      getQuery() {
        this.fullscreenLoading = true;
        axios.post('/api/query-group', { user_id: this.$route.params.userid }, {
          headers: { tokens: sessionStorage.getItem('token') },
        })
          .then((res) => {
            if (res.data.status) {
              //               data { status, message, group_list }
              // group_list [{ “id：群组ID”, “group_name：群组名字”, “admin”：用户是否是群主},...]
              this.grouplist = res.data.group_list;
              this.$emit('defaultGroup', this.grouplist[0]);
              this.fullscreenLoading = false;
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
      createGroup() {
        this.$prompt('为你的新群取一个好听的名字', '群组创建', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          if (value === null) {
            // eslint-disable-next-line
            value = '';
          }
          axios.post('/api/create-group', { user_id: this.$route.params.userid, group_name: value }, {
            headers: { tokens: sessionStorage.getItem('token') },
          })
            .then((res) => {
              // eslint-disable-next-line no-unused-vars
              let str;
              let messagetype;
              if (res.data.status) {
                this.grouplist.push({ id: res.data.group_id, group_name: value, admin: true });
                messagetype = 'success';
                str = `成功创建群组，名为：${value} 邀请码为 ${res.data.invite_key}`;
                // eslint-disable-next-line no-empty
              } else {
                str = '创建失败';
                messagetype = 'warning';
              }
              this.$message({
                type: messagetype,
                message: str,
              });
            })
            .catch((err) => {
              console.log(err);
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入',
          });
        });
      },
      joinGroup() {
        this.$prompt('输入邀请码', '加入', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          axios.post('/api/join-group', { user_id: this.$route.params.userid, invite_key: value }, {
            headers: { tokens: sessionStorage.getItem('token') },
          })
            .then((res) => {
              // eslint-disable-next-line no-unused-vars
              let str;
              let messagetype;
              if (res.data.status) {
                str = '成功加入';
                messagetype = 'success';
                this.getQuery();
              } else {
                str = '加入失败';
                messagetype = 'warning';
              }
              this.$message({
                type: messagetype,
                message: str,
              });
            })
            .catch((err) => {
              console.log(err);
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入',
          });
        });
      },
    },
  created() {
    this.getQuery();
  },
};
</script>
<style>
.group-list{
  margin-top: 10px;
}
.el-col-3{
  transition: all .2s ease-in-out;
}
.el-col-3:hover{
  transform: scale(1.05);
  z-index: 1;
}
</style>
