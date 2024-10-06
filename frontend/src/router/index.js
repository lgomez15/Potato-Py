// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import PerformanceView from '../views/PerformanceView.vue';
import Dashboard from '../views/Dashboard.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard,
  },
  {
    path: '/performance',
    name: 'Performance',
    component: PerformanceView,
  },
  // Puedes agregar más rutas si es necesario
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
