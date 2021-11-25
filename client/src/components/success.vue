<template>
  <div class="container">
    <el-empty description="描述文字"></el-empty>
    <label>{{ msg }}</label>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Success',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = '/api/success';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
