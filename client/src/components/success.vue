<template>
  <div class="container">
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
