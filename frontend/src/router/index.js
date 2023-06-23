import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../components/SignupUser.vue')
  },{
    path: '/createlist',
    name: 'createList',
    component: () => import('../components/createList.vue')
  },
  {
    path: '/:name/newcard',
    name: 'createCard',
    component: () => import('../components/createCard.vue')
  },
  {
    path: '/:id/updatecard',
    name: 'editCard',
    component: () => import('../components/editCard.vue')
  },
  {
    path: '/:name/editlist',
    name: 'editList',
    component: () => import('../components/editList.vue')
  },
  {
    path:'/summary',
    name:'summary',
    component: () => import('../components/summary.vue')
  },
  {
    path: '/login',
    name: 'login', 
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../components/LoginUser.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
