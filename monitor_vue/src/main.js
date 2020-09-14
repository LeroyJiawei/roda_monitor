// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './style/reset.css';
import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App';
import routes from './router';

// store为实例化生成的
import store from './store';
import Config from './config/index';
import Sto from 'store';

// axios
import axios from "axios";

// element-ui
import ElementUI from "element-ui";
// import "element-ui/lib/theme-chalk/index.css";

Vue.use(VueRouter);
Vue.use(ElementUI);

window.$config = {};
window.$config.HOST = 'http://localhost:80';
// window.$config.HOST = ''; // production

// import { Message, loading } from 'element-ui';

Vue.prototype.$axios = axios;
// Vue.prototype.$loading = loading;
// Vue.prototype.$message = Message;
Vue.prototype.$sto = Sto;
Vue.prototype.$conf = Config;

Vue.config.productionTip = false

// 创建路由实例
const router = new VueRouter({
  routes: routes,
  mode: 'history',
  strict: process.env.NODE_ENV === 'development' // 生产环境使用严格模式
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
