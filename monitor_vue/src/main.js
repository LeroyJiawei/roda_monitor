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
// import VueAxios from 'vue-axios';
// element-ui
import ElementUI from "element-ui";
// import "element-ui/lib/theme-chalk/index.css";

// import Enum from 'vue-enum'
// let enumInfo = {
//   SOURCE_IN_TYPE: {
//       PURCHASE_IN: {
//           value: 1,
//           desc: 'supernode'
//       },
//       REFUND_IN: {
//           value: 2,
//           desc: 'source-edge'
//       },
//       CHECK_IN: {
//           value: 3,
//           desc: 'sink-edge'
//       },
//       CONFIRM_IN: {
//           value: 4,
//           desc: 'hub-edge'
//       },
//       CONFIRM_IN: {
//         value: 5,
//         desc: 'web-edge'
//     },
//     CONFIRM_IN: {
//       value: 6,
//       desc: 'all'
//   }
//   }
// };
// Vue.use(Enum,{enumInfo});
// Vue.prototype.$enum = Enum;

Vue.use(VueRouter);
Vue.use(ElementUI);

window.$config = {};
// window.$config.HOST = 'https://easy-mock.com/mock/5f6736c27304034f4b7541d4'
window.$config.HOST = 'http://192.168.0.107';
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
