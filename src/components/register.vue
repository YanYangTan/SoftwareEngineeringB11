<template>
  <div class="container">
    <el-card>
    <el-form :model="userForm" :rules="rules" ref="userForm" label-width="120px" class="demo-userForm"><img class="logo" src="../assets/logo.jpg" alt=logo/ width=260 length=260/>
      <el-form-item label="Username" prop="username">
        <el-input v-model="userForm.username"></el-input>
      </el-form-item>
    <el-form-item label="Password" prop="password">
    <el-input v-model="userForm.password" show-pasword></el-input>
  </el-form-item>
          <el-form-item label="Email" prop="email">
    <el-input v-model="userForm.email"></el-input>
  </el-form-item>
      <el-form-item label="Phone" prop="phone">
    <el-input v-model="userForm.phone"></el-input>
  </el-form-item>
<!--sadcommenthere-->
  <el-form-item label="Birthdate" required>
      <el-form-item prop="birthdate">
        <el-date-picker default-value="2000-01-01"
                  editable="false"
                  type="date"
                  contenteditable="false"
                  v-model="userForm.birthday" style="width: 100%;"></el-date-picker>
      </el-form-item>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="register">Register</el-button>
    <el-button @click="home">Home</el-button>
  </el-form-item>
</el-form></el-card>
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
      rules: {
        username: [
          { required: true, message: 'Please input Username', trigger: 'blur' },
          {
            min: 6, max: 16, message: 'Length should be 6 to 16', trigger: 'blur',
          },
        ],
        password: [
          { required: true, message: 'Please input Password', trigger: 'blur' },
          {
            min: 6, max: 32, message: 'Length should be 6 to 32', trigger: 'blur',
          },
        ],
        email: [
          { required: true, message: 'Please input Email', trigger: 'blur' },
        ],
        phone: [
          { required: true, message: 'Please input Phone', trigger: 'blur' },
          {
            min: 6, max: 16, message: 'Length should be 6 to 16', trigger: 'blur',
          },
        ],
      },
    };
  },
  methods: {
    register() {
      axios.post('/api/register', {
        username: this.userForm.username,
        password: this.userForm.password,
        email: this.userForm.email,
        phone: this.userForm.phone,
        birthday: this.userForm.birthday,
      });
      this.$router.push('/');
      // .then((res) => {
      //   if (res.data.status) {
      //     this.$router.push('/');
      //   }
      // })
      // .catch((err) => {
      //   console.log(err);
      // });
    },
    home() {
      this.$router.push('/');
    },
  },
};
</script>
