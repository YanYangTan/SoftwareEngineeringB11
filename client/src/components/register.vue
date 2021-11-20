<template>
    <div class="vue-template">
      <el-card class="carrd">
        <form @submit.prevent="register">
            <h3>Register</h3>
            <div class="form-group">
                <label>Username</label>
                <input type="username" required class="form-control form-control-lg" v-model="userForm.username"/>
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" required  class="form-control form-control-lg" v-model="userForm.password"/>
            </div>
<!--hihi-->
          <div class="form-group">
                <label>Email</label>
                <input type="email" required class="form-control form-control-lg" v-model="userForm.email"/>
            </div>

          <div class="form-group">
                <label>Phone</label>
                <input type="number" required class="form-control form-control-lg" v-model="userForm.phone"/>
            </div>

          <div class="form-group">
                <label>Birthday</label>
                <input type="date" required class="form-control form-control-lg" v-model="userForm.birthday"/>
            </div>

            <button type="submit" class="btn btn-dark btn-lg btn-block">register</button>
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
        email: '',
        phone: '',
        birthday: '',
      },
    };
  },
  methods: {
    register() {
      axios.post('/api/register', {
        username: this.userForm.username, password: this.userForm.password, email: this.userForm.email, phone: this.userForm.phone, birthday: this.userForm.birthday,
      })
        .then((res) => {
          console.log(res.data.message);
          if (res.data.status) {
            this.$router.push('/');
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    temp() {
      this.$router.push('/');
    },
  },
};
</script>
