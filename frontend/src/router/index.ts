import Vue from "vue";
import Router from "vue-router";
import LoginVue from '../account/Login.vue';
import HelloWorld from '../components/HelloWorld.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: 'login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginVue
    },
    {
      path: '/hello',
      name: 'hello',
      component: HelloWorld
    }
  ]
})
