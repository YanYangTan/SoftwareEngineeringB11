<template>
  <!--add a profile pic here-->
  <div>
  <div class=info>
<el-descriptions title="User Info">
    <el-descriptions-item label="Username">{{ username }}</el-descriptions-item>
    <el-descriptions-item label="Telephone">{{phone}}</el-descriptions-item>
    <el-descriptions-item label="Birthday">{{ birthday }}</el-descriptions-item>
    <el-descriptions-item label="Quote">{{quote}}</el-descriptions-item>
</el-descriptions>
  </div>
  <el-row>
  <el-button type="text" @click="changeQuote">Edit quote</el-button>
    <el-button type="text" @click="changeNumber">CHange Number</el-button>
  </el-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'profile',
  data() {
    return {
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
            // console.log(this.birthday);
          } else {
            console.log(res.data.message);
          }
        });
    },
    changeQuote() {
      this.$prompt('change your quote lamooooo', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        axios.post('/api/save-userinfo', { user_id: this.$route.params.userid, phone: this.phone, quote: value })
          .then((res) => {
            if (res.data.status) {
              this.getUserInfo();
              console.log('Success!');
            }
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
      this.$prompt('change your number geiiiii', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        axios.post('/api/save-userinfo', { user_id: this.$route.params.userid, phone: value, quote: this.quote })
          .then((res) => {
            if (res.data.status) {
              this.getUserInfo();
              console.log('Success!');
            }
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
