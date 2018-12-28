import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home'
import Word from '../components/word/Word'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/word',
      name: 'Word',
      component: Word
    },
  ]
});
