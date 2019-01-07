import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home'
import Word from '../components/word/Word'
import SignIn from '../components/sign/SignIn'
import SignUp from '../components/sign/SignUp'
import TRoutes from './test'
import Comm from '../components/communicate/Comm'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    ...TRoutes//测试用的路由.这里是数组解包
    , {
      path: '/',
      name: 'Home',
      component: Home
    }, {
      path: '/word',
      name: 'Word',
      component: Word
    }, {
      path: '/sign-in',
      name: 'SignIn',
      component: SignIn
    }, {
      path: '/sign-up',
      name: 'SignUp',
      component: SignUp
    }, {
      path: '/comm',
      name: 'Comm',
      component: Comm
    }
  ]
});
