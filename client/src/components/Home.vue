<template>
    <div class="vue-template">
<el-card>
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
          <button type="login" class="btn btn-black btn-lg btn-block">Register</button>
        </div>
      </form>
  </el-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
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
          console.log(res.data.message);
          if (res.data.status) {
            this.$router.push('/success');
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
