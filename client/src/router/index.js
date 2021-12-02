import Vue from 'vue';
import Router from 'vue-router';
import Success from '../components/success.vue';
import Home from '../components/Home.vue';
import Register from '../components/register.vue';
import MainPage from '../components/MainPage.vue';

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
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/main',
      name: "MainPage",
      component: MainPage,
    },
  ],
});
