<template>
  <!--add a profile pic here-->
  <div v-loading.fullscreen.lock="fullscreenLoading">
    <div class="demo-image" >
  <img
    style="margin-left:-21px;margin-top:-20px;width: 103%; height: 300px;"
    src="https://resilientblog.co/wp-content/uploads/2019/07/sky-quotes.jpg" />
      </div>
    <div style="z-index: 1">
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                 style="margin-top: -70px;"  :size="120"></el-avatar>
    </div>
<!--        <div class="demo-image" >-->
<!--  <el-image-->
<!--    style="margin-left:-21px;margin-top:-20px;width: 120%; height: 300px;" :z-index="this.zinn"-->
<!--    src="https://resilientblog.co/wp-content/uploads/2019/07/sky-quotes.jpg" >-->
<!--  </el-image>-->
<!--      </div>-->
<!--  <div class=info>-->
<!--<el-descriptions title="User Info"-->
<!--v-loading="loading">-->
<!--    <el-descriptions-item label="Username">{{ username }}</el-descriptions-item>-->
<!--    <el-descriptions-item label="Telephone">{{phone}}</el-descriptions-item>-->
<!--    <el-descriptions-item label="Birthday">{{ birthday }}</el-descriptions-item>-->
<!--    <el-descriptions-item label="Quote">{{quote}}</el-descriptions-item>-->
<!--</el-descriptions>-->
<!--  </div>-->
    <h1 style="margin-left: 10px">{{ username }}</h1>
    <div style="width:100%">
    <el-card style="margin-top: 40px">
      <span >电话号码 : </span><span style="color: #4714ff">  {{phone}}</span><span style="margin-left: 29%">电子邮件    :   </span><span style="color: #4714ff"> {{ email }}</span>
    </el-card>
    <el-card style="margin-top: 10px">
      <span>生日日期    :   </span><span style="color: #4714ff"> {{ birthday }}</span><span style="margin-left: 30%">标语    :     </span><span style="color: #4714ff"> {{quote}}</span>
    </el-card>
<!--    <el-card style="margin-top: 10px">-->
<!--      <span>标语    :     {{quote}}</span>-->
<!--    </el-card>-->
      </div>
  <el-row>
    <el-button type="text" @click="changeNumber">更换电话号码</el-button>
    <el-button type="text" @click="changeQuote">更改标语</el-button>
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
      fullscreenLoading: true,
    };
  },
  methods: {
    getUserInfo() {
      this.fullscreenLoading = true;
      this.id = this.$route.params.userid;
      console.log(this.$route.params.userid);
      console.log('what is going on');
      axios.post('/api/query-userinfo', { user_id: this.$route.params.userid }, {
        // headers: { tokens: sessionStorage.getItem('token') },
        headers: { tokens: localStorage.getItem('token') },
      })
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
          this.fullscreenLoading = false;
        });
    },
    changeQuote() {
      this.$prompt('输入新标语', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        let str;
        let messagetype;
        axios.post('/api/save-userinfo', { user_id: this.$route.params.userid, phone: this.phone, quote: value }, {
          // headers: { tokens: sessionStorage.getItem('token') },
          headers: { tokens: localStorage.getItem('token') },
        })
          .then((res) => {
            if (res.data.status) {
              messagetype = 'success';
              str = '成功修改';
              this.getUserInfo();
            } else {
              messagetype = 'warning';
              str = '标语不合法';
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
      this.$prompt('输入新手机号', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        let str;
        let messagetype;
        axios.post('/api/save-userinfo', { user_id: this.$route.params.userid, phone: value, quote: this.quote }, {
          // headers: { tokens: sessionStorage.getItem('token') },
          headers: { tokens: localStorage.getItem('token') },
        })
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
