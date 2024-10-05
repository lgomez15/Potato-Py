<script setup>
import ControlPanel from '../components/ControlPanel.vue'; // Ajusta la ruta
import WeatherBar from '@/components/WeatherBar.vue';

// Variables que representan la fecha y la ubicación
const datetime = new Date().toISOString(); // Obtiene la fecha y hora actual en formato ISO
const latitude = 40.4167047; // Latitud de ejemplo (Madrid)
const longitude = -3.7035825; // Longitud de ejemplo (Madrid)
</script>

<template>
  <div class="dashboard">

    <ControlPanel :datetime="datetime" :latitude="latitude" :longitude="longitude" />
  </div>
</template>
  
<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f2f2f2; /* Color de fondo del panel */
}
</style>
