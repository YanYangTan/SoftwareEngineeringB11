import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
// eslint-disable-next-line import/no-extraneous-dependencies
import ElementUI from 'element-ui';
// eslint-disable-next-line import/no-extraneous-dependencies
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import '@/assets/css/main.css';

Vue.use(BootstrapVue);
Vue.use(ElementUI);
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
