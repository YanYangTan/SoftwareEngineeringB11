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

    </el-container>
  </el-header>
  <el-container>
    <el-aside width="300px">
      <MemberList :info="this.$props.info"></MemberList>
    </el-aside>

    <el-main>
      <div class="genealogy">
      <GenealogyPage :info="this.$props.info" style="height:70%"></GenealogyPage>
    </div>
    </el-main>

  </el-container>
    <el-footer height="0px">
      <el-button  style="position: absolute; bottom: 10px; right: 250px;" v-if="this.$props.info.admin" type="primary" icon="el-icon-share" @click="getInviteKey">获取邀请码</el-button>
      <el-button style="position: absolute; bottom: 10px; right: 130px;" v-if="this.$props.info.admin" type="danger" icon="el-icon-delete"  @click="DeleteGroup">删除群</el-button>
      <el-button  style="position: absolute; bottom: 10px; right: 10px;" type="danger" icon="el-icon-warning" @click="leaveGroup">退出群</el-button>
    </el-footer>
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
      axios.post('/api/delete-group', { group_id: this.$props.info.id })
        .then((res) => {
          if (res.data.status) {
            this.$emit('BacktoGroupList');
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    BackToGroupList() {
      this.$emit('BacktoGroupList');
    },
    getInviteKey() {
      axios.post('/api/generate-key', { group_id: this.$props.info.id })
        .then((res) => {
          if (res.data.status) {
            this.invitekey.num = res.data.invite_key;
            this.invitekey.ex_date = res.data.key_expiry_date;
            console.log(this.invitekey);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    leaveGroup() {
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
    },
  },
  created() {
    this.checkAdmin();
    console.log(this.$props.info);
  },
};
</script>

<style scoped>
.genealogy{
  height: 80%;
}
</style>
