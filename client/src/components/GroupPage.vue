<template>
  <el-container>
  <el-header>
    <el-container>
    <el-button
      style="width: 50px;margin-right: 30px;"
      icon="el-icon-back"
      @click="BackToGroupList" circle></el-button>
    <h1>{{this.$props.info.group_name}}</h1>
    </el-container>
  </el-header>
  <el-container>
    <el-aside width="300px">
      <MemberList :info="this.$props.info"></MemberList>
    </el-aside>
    <el-main>
      <GenealogyPage></GenealogyPage>
    </el-main>
  </el-container>
    <el-footer >
       <el-button style="position: absolute; bottom: 10px; right: 10px;" v-if="this.$props.info.admin" type="danger" icon="el-icon-delete"  @click="DeleteGroup">删除群</el-button>
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
    };
  },
  methods: {
    checkAdmin() {
      axios.post('/api/query-admin', { group_id: this.$props.info.id, user_id: this.$route.params.userid })
        .then((res) => {
          if (res.data.status) {
            this.$props.info.admin = res.data.admin;
            console.log(this.$props.info.admin);
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
  },
  created() {
    this.checkAdmin();
  },
};
</script>

<style scoped>

</style>
