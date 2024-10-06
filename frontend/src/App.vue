<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue'; // Asegúrate de que la ruta sea correcta
import Dashboard from './views/Dashboard.vue';
import Chat from './components/Chat.vue'; // Asegúrate de que "Chat.vue" coincide exactamente
</script>

<template>
  <div>
    <Chat />
    <Navbar /> <!-- Aquí agregas el Navbar -->
    <RouterView />
  </div>
</template>
