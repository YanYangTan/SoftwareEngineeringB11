import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
// eslint-disable-next-line import/no-extraneous-dependencies
import Vuetify from 'vuetify';
import DaySpanVuetify from 'dayspan-vuetify';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import '@/assets/css/main.css';
// eslint-disable-next-line import/order
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// eslint-disable-next-line import/no-extraneous-dependencies
import 'vuetify/dist/vuetify.min.css';
// eslint-disable-next-line import/no-extraneous-dependencies
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'dayspan-vuetify/dist/lib/dayspan-vuetify.min.css';

Vue.use(ElementUI);
Vue.use(BootstrapVue);
Vue.use(Vuetify);
Vue.use(DaySpanVuetify, {
  methods: {
    getDefaultEventColor: () => '#1976d2',
  },
});
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
  el: '#app',
  components: { App },
  template: '<App/>',
}).$mount('#app');
