<template>
  <div>
    <label>{{this.$route.params.userid}}</label>
  </div>
</template>

<script>
// import MainPage from './MainPage.vue';

export default {
  name: 'GroupList',
  // components: {
  //   // eslint-disable-next-line vue/no-unused-components
  //   MainPage,
  // },
  data() {
    return {
      // userid: '',
      msg: '',
    };
  },
  methods: {
  },
  created() {
    // console.log(userid);
  },
};
</script>

<style scoped>

</style>
