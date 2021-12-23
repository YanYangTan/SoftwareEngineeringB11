<template>
    <div class="vue-template">
      <div class="bg">
      </div>
      <div class="sidebar">
        <div class="side-form">
          <form @submit.prevent="login">
              <h3>登录</h3>

              <div class="form-group">
                  <label>用户</label>
                  <input type="username" class="form-control form-control-lg" v-model="userForm.username"/>
              </div>

              <div class="form-group">
                  <label>密码</label>
                  <input type="password" class="form-control form-control-lg" v-model="userForm.password"/>
              </div>

              <button type="login" class="btn btn-dark btn-lg btn-block">登录</button>
          </form>
        <form @submit.prevent="register">
          <div class="form-group">
            <span>还未注册？ </span>
            <el-button type="text" @click="register ">注册</el-button>
          </div>
        </form>
      </div>
     </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loginpath: '/success/',
      userForm: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      axios.post('/api/login', { username: this.userForm.username, password: this.userForm.password })
        .then((res) => {
          if (res.data.status) {
            window.sessionStorage.setItem('token', res.data.token);
            this.loginpath = '/success/';
            this.loginpath += String(res.data.userid);
            this.loginpath += '/';
            this.loginpath += String(this.$data.userForm.username);
            this.$router.push(this.loginpath);
          } else {
            this.$message({
              type: 'warning',
              message: '用户名或密码错误！',
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    register() {
      this.$router.push('/register');
    },
  },
};
</script>
