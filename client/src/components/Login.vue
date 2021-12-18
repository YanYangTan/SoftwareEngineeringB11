<template>
    <div class="vue-template">
      <div class="bg">
      </div>
      <div class="sidebar">
        <div class="side-form">
          <form @submit.prevent="login">
              <h3>Sign In</h3>

              <div class="form-group">
                  <label>Username</label>
                  <input type="username" class="form-control form-control-lg" v-model="userForm.username"/>
              </div>

              <div class="form-group">
                  <label>Password</label>
                  <input type="password" class="form-control form-control-lg" v-model="userForm.password"/>
              </div>

              <button type="login" class="btn btn-dark btn-lg btn-block">Sign In</button>
          </form>
        <form @submit.prevent="register">
          <div class="form-group">
            <span>Not Registered yet? </span>
            <el-button type="text" @click="register ">Register</el-button>
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
      let str;
      axios.post('/api/login', { username: this.userForm.username, password: this.userForm.password })
        .then((res) => {
          if (res.data.status) {
            this.loginpath += String(res.data.userid);
            this.loginpath += '/';
            this.loginpath += String(this.$data.userForm.username);
            this.$router.push(this.loginpath);
          } else {
            str = res.data.message;
            this.$message({
              type: 'warning',
              message: str,
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
