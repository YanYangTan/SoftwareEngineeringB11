<template>
  <div>
    <v-app id="dayspan" v-cloak>
    <ds-calendar-app :calendar="calendar"></ds-calendar-app>
  </v-app>
  </div>
</template>

<script>
// import MainPage from './MainPage.vue';
// eslint-disable-next-line import/no-extraneous-dependencies
import { Calendar } from 'dayspan';

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
      calendar: Calendar.months(),
    };
  },
  methods: {
  },
  created() {
    // console.log(userid);
  },
};
</script>

<style>
body, html, #app, #dayspan {
  font-family: Roboto, sans-serif;
  width: 100%;
  height: 100%;
}
</style>
