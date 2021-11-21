import Vue from 'vue';
import Router from 'vue-router';
import Success from '../components/MainPage.vue';
import Login from '../components/Login.vue';
import Register from '../components/register.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/success/:userid',
      name: 'Success',
      component: Success,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },

  ],
});
