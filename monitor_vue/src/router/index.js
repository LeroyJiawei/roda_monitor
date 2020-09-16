import Config from '../config/index';

const E2E = r => require.ensure([], () => r(require('../page/perfomance/e2e')), 'e2e');
const Topo = r => require.ensure([], () => r(require('../page/topo')), 'topo');
const N2N = r => require.ensure([], () => r(require('../page/n2n')), 'n2n');
const Hub = r => require.ensure([], () => r(require('../page/hub')), 'hub');

//---------------------
const Login = r => require.ensure([], () => r(require('../page/user/login')), 'login');
const Layout = r => require.ensure([], () => r(require('../page/layout')), 'layout');

// 快速入门
const Quick = r => require.ensure([], () => r(require('../page/quick/quick')), 'quick');
// 基础服务 -- 三级菜单 -- 文章管理
const Article = r => require.ensure([], () => r(require('../page/base/thrmenu/article')), 'article');
// 基础服务 -- 三级菜单 -- 评论管理
const Comment = r => require.ensure([], () => r(require('../page/base/thrmenu/comment')), 'comment');
// // 基础服务 -- 三级菜单 -- 用户留存
// const Left = r => require.ensure([], () => r(require('../page/base/thrmenu/left')), 'left');
// // 基础服务 -- 三级菜单 -- 流失用户
// const Lost = r => require.ensure([], () => r(require('../page/base/thrmenu/lost')), 'lost');

// // 用户中心 -- 用户管理
// const User = r => require.ensure([], () => r(require('../page/user/user')), 'user');

// 基础服务 -- 三级菜单
const thrmenuNavbar = [{
  title: 'filter1',
  index: '/thrmenu/filter1'
}, {
  title: 'filter2',
  index: '/thrmenu/filter2'
}, {
  title: 'filter3',
  index: '/thrmenu/filter3'
}, {
  title: 'filter4',
  index: '/thrmenu/filter4'
}];

export default [
  {
  path: Config.route.login,
  name: 'Login',
  component: Login
}, {
  path: '/',
  name: 'Layout',
  component: Layout,
  children: [
    { // 快速入门
    path: '/quick',
    name: 'Quick',
    component: Quick,
    meta: {
      bcrumd: ['快速入门']
    }
    }, 
    { // 基础服务 -- 三级菜单 -- 文章管理
      path: '/thrmenu/filter1',
      name: 'E2E',
      component: E2E,
      meta: {
        activePath: '/thrmenu/filter1',
        bcrumd: ['性能', '三级菜单', 'filter1'],
        navbar: thrmenuNavbar
      }
    }, { // 基础服务 -- 三级菜单 -- 评论管理
      path: '/thrmenu/filter2',
      name: 'Comment',
      component: Comment,
      meta: {
        activePath: '/thrmenu/filter2',
        bcrumd: ['性能', '三级菜单', 'filter2'],
        navbar: thrmenuNavbar
      }
    },{
      path: '/thrmenu/filter3',
      name: 'Comment',
      component: Comment,
      meta: {
        activePath: '/thrmenu/filter3',
        bcrumd: ['性能', '三级菜单', 'filter3'],
        navbar: thrmenuNavbar
      }
    },
    {
      path: '/thrmenu/filter4',
      name: 'Comment',
      component: Comment,
      meta: {
        activePath: '/thrmenu/filter4',
        bcrumd: ['性能', '三级菜单', 'filter4'],
        navbar: thrmenuNavbar
      }
    },
    { 
      path: '/perfomance/e2e',
      name: 'E2E',
      component: E2E,
      meta: {
        bcrumd: ['性能','端到端']
      }
    },
    { 
      path: '/topo',
      name: 'Topo',
      component: Topo,
      meta: {
        bcrumd: ['拓扑']
      }
    },
    { 
      path: '/n2n',
      name: 'N2N',
      component: N2N,
      meta: {
        bcrumd: ['N2N']
      }
    },
    { 
      path: '/hub',
      name: 'Hub',
      component: Hub,
      meta: {
        bcrumd: ['Hub']
      }
    }]
}, {
  path: '*',
  redirect: Config.route.login,
  name: 'Login',
  component: Login
}]
