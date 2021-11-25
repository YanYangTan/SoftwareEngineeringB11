<template>
    <div class="vue-template">
      <div class="bg">
      </div>
      <div class="sidebar">
        <div class="side-form">
<!--      <el-card class="carrd">-->
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
        <span>Registered? </span>
        <el-button type="text" @click="SignIn">Sign In</el-button>
<!--        </el-card>-->
           </div>
         </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterPage',
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
    inputjudge(message) {
      // eslint-disable-next-line no-unused-vars
      let temp;
      if (message === 'username') {
        temp = '用户名非法（6~10位）';
      } else if (message === 'Username occupied!') {
        temp = '此用户名已存在！';
      } else if (message === 'password') {
        temp = '密码非法（至少包含大小写，数字的6~18位数字）';
      } else if (message === 'email') {
        temp = '邮箱非法';
      } else if (message === 'Email occupied!') {
        temp = '邮箱已注册！';
      } else if (message === 'birthday') {
        temp = '生日非法';
      } else if (message === 'Registered!') {
        temp = '成功注册！';
      }
      this.$alert(temp, '提示', {
        confirmButtonText: '确定',
      });
    },
    register() {
      axios.post('/api/register', {
        username: this.userForm.username, password: this.userForm.password, email: this.userForm.email, phone: this.userForm.phone, birthday: this.userForm.birthday,
      })
        // eslint-disable-next-line no-shadow
        .then((res) => {
          console.log(res.data.message);
          // eslint-disable-next-line no-empty
          if (!res.data.status) {
            this.inputjudge(res.data.message);
          } else {
            this.$router.push('/');
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    SignIn() {
      this.$router.push('/');
    },
    created() {
    },
  },
};
</script>

<style scoped>

.side-form {
  padding:20%;
  padding-top:10%;
  margin-top: 0%;
}

</style>
