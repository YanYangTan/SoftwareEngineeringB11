import Vue from 'vue';
import Router from 'vue-router';
import Success from '../components/success.vue';
import Home from '../components/Home.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/success',
      name: 'Success',
      component: Success,
    },
  ],
});
