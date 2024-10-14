import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      redirect: to => {
        return { path: '/home'}
      },
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path: '/404',
      name: '404',
      component: () => import('../views/404.vue')
    },
    {
      path: '/:catchAll(.*)',
      name: 'error',
      redirect: '/404',
    }
  ]
})

export default router
