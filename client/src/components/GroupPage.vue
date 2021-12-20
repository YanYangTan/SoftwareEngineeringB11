<template>
  <el-container>
  <el-header>
    <el-container>
    <el-button
      style="width: 50px;margin-right: 30px;"
      icon="el-icon-back"
      @click="BackToGroupList" circle></el-button>
    <h1>{{this.$props.info.group_name}}
    </h1>
 <el-button  style="position: absolute; top: 10px; right: 10px;" type="primary" icon="el-icon-edit" @click="changeGroupName">更改群名</el-button>
    </el-container>
  </el-header>
  <el-container>
    <el-aside width="300px">
      <MemberList :info="this.$props.info"></MemberList>
    </el-aside>
    <div id="elmain">
<!--    <el-main id="elmain">-->
      <GenealogyPage :info="this.$props.info"></GenealogyPage>
<!--    </el-main>-->
    </div>
  </el-container>
      <el-button  style="position: absolute; bottom: 10px; right: 239px;" v-if="this.$props.info.admin" type="primary" icon="el-icon-share" @click="getInviteKey">获取邀请码</el-button>
      <el-button style="position: absolute; bottom: 10px; right: 124px;" v-if="this.$props.info.admin" type="danger" icon="el-icon-delete"  @click="DeleteGroup">删除群</el-button>
      <el-button  style="position: absolute; bottom: 10px; right: 10px;" type="danger" icon="el-icon-warning" @click="leaveGroup">退出群</el-button>
</el-container>
</template>

<script>
import axios from 'axios';
import MemberList from './MemberList.vue';
import GenealogyPage from './GenealogyPage.vue';

export default {
  name: 'GroupPage',
  components: { GenealogyPage, MemberList },
  Component: {
    MemberList,
    GenealogyPage,
  },
  props: {
    info: {},
  },
  data() {
    return {
      userid: '',
      invitekey: { num: '', ex_date: '' },
    };
  },
  methods: {
    changeGroupName() {
      this.$prompt('为你的群改一个好听的名字', '群名更改', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        if (value === null) {
          // eslint-disable-next-line
            value = '';
        }
        axios.post('/api/change-groupname', { group_id: this.$props.info.id, new_name: value })
          .then((res) => {
            // eslint-disable-next-line no-unused-vars
            let str;
            let messagetype;
            if (res.data.status) {
              messagetype = 'success';
              str = `成功更改群名，名为：${value}`;
              this.$props.info.group_name = value;
              // eslint-disable-next-line no-empty
            } else {
              str = '更改失败';
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
    checkAdmin() {
      axios.post('/api/query-admin', { group_id: this.$props.info.id, user_id: this.$route.params.userid })
        .then((res) => {
          if (res.data.status) {
            this.$props.info.admin = res.data.admin;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    DeleteGroup() {
      // eslint-disable-next-line
      if (confirm('确定删除群？')) {
        axios.post('/api/delete-group', { group_id: this.$props.info.id })
          .then((res) => {
            let str;
            let messagetype;
            if (res.data.status) {
              str = '成功删除群';
              messagetype = 'success';
              this.$emit('BacktoGroupList');
            } else {
              str = '删除群失败';
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
      }
    },
    BackToGroupList() {
      this.$emit('BacktoGroupList');
    },
    getInviteKey() {
      let str;
      axios.post('/api/generate-key', { group_id: this.$props.info.id })
        .then((res) => {
          if (res.data.status) {
            this.invitekey.num = res.data.invite_key;
            this.invitekey.ex_date = res.data.key_expiry_date;
            console.log(this.invitekey);
            // eslint-disable-next-line
            str = '新的邀请码是' + this.invitekey.num + '，将于' + this.invitekey.ex_date + '过期';
            this.$message({
              type: 'success',
              message: str,
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    leaveGroup() {
      // eslint-disable-next-line
      if (confirm('确定退群？')) {
        axios.post('/api/leave-group', {
          group_id: this.$props.info.id,
          user_id: this.$route.params.userid,
        })
          .then((res) => {
            // eslint-disable-next-line no-empty
            if (res.data.status) {
              this.BackToGroupList();
              this.$message({
                type: 'success',
                message: '成功退出群组',
              });
            } else {
              this.$message({
                type: 'warning',
                message: '无法退群',
              });
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
  created() {
    this.checkAdmin();
    console.log(this.$props.info);
  },
};
</script>

<style scoped>
#elmain{
  /*position: absolute;*/
  margin-top: -55px;
  margin-left: 5px;
  width: 100%;
  height: 100%;
}
</style>
