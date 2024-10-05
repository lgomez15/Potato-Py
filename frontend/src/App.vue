<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue'; // Asegúrate de que la ruta sea correcta
import Dashboard from './views/Dashboard.vue';
</script>

<template>
  <div>
    <Navbar /> <!-- Aquí agregas el Navbar -->
    <RouterView />
  </div>
</template>
