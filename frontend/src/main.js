import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import RegisterUser from './components/RegisterUser.vue'

const routes = [
  { path: '/', component: HelloWorld },
  { path: '/register', component: RegisterUser}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App);
app.use(router);
app.mount('#app');
