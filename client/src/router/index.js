import Vue from 'vue';
import Router from 'vue-router';
import MainPage from '../components/MainPage.vue';
import Login from '../components/Login.vue';
import Register from '../components/register.vue';
import Calender from '../components/Calender.vue';

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
      path: '/success/:userid/:username',
      name: 'Success',
      component: MainPage,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/Calender/:groupid',
      name: 'Calender',
      component: Calender,
    },

  ],
});
