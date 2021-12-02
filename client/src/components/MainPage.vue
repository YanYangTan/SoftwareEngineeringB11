<template>
  <div class="container">
<!--    <el-empty description="描述文字"></el-empty>-->
    <label>个人信息</label>
<!--    <el-button size="mini" style="float:right" type="primary" @click="save">保存当前标注</el-button>-->
    <!-- 下面如果改成v-if就无法监控变量 -->
    <label>{{this.$route.params.userid}}</label>
          <GroupList

          ></GroupList>

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
  },
  created() {
    this.getMessage();
  },
};
</script>
