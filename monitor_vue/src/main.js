// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './style/reset.css';
import Vue from 'vue';

import VueRouter from 'vue-router';
import App from './App';
import routes from './router';

/* echats begin */
// import ECharts from 'vue-echarts' // 在 webpack 环境下指向 components/ECharts.vue
// 手动引入 ECharts 各模块来减小打包体积
// import 'echarts/lib/chart/bar'
// import 'echarts/lib/component/tooltip'
// 如果需要配合 ECharts 扩展使用，只需要直接引入扩展包即可
// 以 ECharts-GL 为例：
// 需要安装依赖：npm install --save echarts-gl，并添加如下引用
// import 'echarts-gl'
// 注册组件后即可使用
// Vue.component('v-chart', ECharts)
/* echats end */

// store为实例化生成的
import store from './store';

import Config from './config/index';

import Sto from 'store';

Vue.use(VueRouter);

import { Message, loading } from 'element-ui';

Vue.prototype.$loading = loading;
Vue.prototype.$message = Message;
Vue.prototype.$sto = Sto;
Vue.prototype.$conf = Config;

Vue.config.productionTip = false

// 创建路由实例
const router = new VueRouter({
  routes: routes,
  mode: 'history',
  strict: process.env.NODE_ENV === 'development' // 生产环境使用严格模式
})

router.beforeEach((to, from, next) => {
  let cookies = Sto.get(Config.constant.cookie);
  if ((!cookies || !cookies.token) && to.path != Config.route.login) {
    next(Config.route.login);
  } else if (cookies && cookies.token && to.path != Config.route.login) {
    let token = cookies.token;
    // 保存2个小时TOKEN
    if ((new Date()).getTime() - token > 7200000) {
      delete cookies.token;
      Sto.set(Config.constant.cookie, cookies);
      next(Config.route.login);
    } else {
      next();
    }
  } else {
    next();
  }
})

router.afterEach((transition) => {
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
