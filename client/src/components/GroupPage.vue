<template>
  <el-container>
  <el-header><h1>{{this.$props.info.group_name}}</h1></el-header>
  <el-container>
    <el-aside width="300px">
      <MemberList :info="this.$props.info"></MemberList>
    </el-aside>
    <el-main>
      <GenealogyPage></GenealogyPage>
    </el-main>
  </el-container>
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
  },
  created() {
    this.checkAdmin();
  },
};
</script>

<style scoped>

</style>
