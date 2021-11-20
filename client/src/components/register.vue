<template>
    <div class="vue-template">
      <el-card class="carrd">
        <form @submit.prevent="register">
            <h3>Register</h3>
            <div class="form-group">
                <label>Username</label>
                <input type="username" minlength="6" maxlength="10" required class="form-control form-control-lg" v-model="userForm.username"/>
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" required minlength="6" maxlength="18" class="form-control form-control-lg" v-model="userForm.password"/>
            </div>
<!--hihi-->
          <div class="form-group">
                <label>Email</label>
                <input type="email" required class="form-control form-control-lg" v-model="userForm.email"/>
            </div>

          <div class="form-group">
                <label>Phone</label>
                <input type="number" min="10000000000" max="99999999999" required class="form-control form-control-lg" v-model="userForm.phone"/>
            </div>

          <div class="form-group">
                <label>Birthday</label>
                <input type="date" id="birthdayID" required class="form-control form-control-lg" v-model="userForm.birthday"/>
                <script type="application/javascript">birthdayID.max = new Date().toISOString().split("T")[0];</script>
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
      const today = new Date().toISOString().substr(0, 10);
      this.querySelector('.userform.Birthday').value = today;
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
