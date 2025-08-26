import { createRouter, createWebHistory } from 'vue-router'
import DisguiseMenu from './pages/DisguiseMenu.vue'
import DisguisePage from './pages/DisguisePage.vue'

const routes = [
  { path: '/', name: 'menu', component: DisguiseMenu },
  {
    path: '/disguise',
    name: 'disguise',
    component: DisguisePage,
    // query → props로 전달
    props: route => ({ target: route.query.target })
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
