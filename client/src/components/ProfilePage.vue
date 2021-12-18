<template>
  <!--add a profile pic here-->
  <div>
  <div class=info>
<el-descriptions title="User Info"
v-loading="loading">
    <el-descriptions-item label="Username">{{ username }}</el-descriptions-item>
    <el-descriptions-item label="Telephone">{{phone}}</el-descriptions-item>
    <el-descriptions-item label="Birthday">{{ birthday }}</el-descriptions-item>
    <el-descriptions-item label="Quote">{{quote}}</el-descriptions-item>
</el-descriptions>
  </div>
  <el-row>
  <el-button type="text" @click="changeQuote">Edit Quote</el-button>
    <el-button type="text" @click="changeNumber">Change Number</el-button>
  </el-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'profile',
  data() {
    return {
      loading: true,
      id: '',
      birthday: '',
      email: '',
      message: '',
      phone: '',
      username: '',
      quote: '',
    };
  },
  methods: {
    getUserInfo() {
      this.id = this.$route.params.userid;
      console.log(this.$route.params.userid);
      console.log('what is going on');
      axios.post('/api/query-userinfo', { user_id: this.$route.params.userid })
        .then((res) => {
          if (res.data.status) {
            console.log('Query success!');
            this.birthday = res.data.birthday;
            this.email = res.data.email;
            this.phone = res.data.phone;
            this.username = res.data.username;
            this.quote = res.data.quote;
            this.loading = false;
          } else {
            console.log(res.data.message);
          }
        });
    },
    changeQuote() {
      this.$prompt('Enter your new quote', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        let str;
        let messagetype;
        axios.post('/api/save-userinfo', { user_id: this.$route.params.userid, phone: this.phone, quote: value })
          .then((res) => {
            if (res.data.status) {
              messagetype = 'success';
              str = '成功修改';
              this.getUserInfo();
            } else {
              messagetype = 'warning';
              str = '电话号码格式错误';
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
    changeNumber() {
      this.$prompt('Enter your new phone number', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        let str;
        let messagetype;
        axios.post('/api/save-userinfo', { user_id: this.$route.params.userid, phone: value, quote: this.quote })
          .then((res) => {
            if (res.data.status) {
              messagetype = 'success';
              str = '成功修改';
              this.getUserInfo();
            } else {
              messagetype = 'warning';
              str = '电话号码格式错误';
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
    this.getUserInfo();
    console.log(this.$route.params.userid);
  },
};
</script>
