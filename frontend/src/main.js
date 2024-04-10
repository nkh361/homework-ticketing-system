import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import LandingPage from './components/IntroductionPage.vue'
import RegisterUser from './components/RegisterUser.vue'
import UserDashboard from './components/UserDashboard.vue'

const routes = [
  { path: '/', name: 'Landing', component: LandingPage },
  { path: '/register', name: 'Register', component: RegisterUser },
  { path: '/dashboard', name: 'Dashboard', component: UserDashboard}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App);
app.use(router);
app.mount('#app');
