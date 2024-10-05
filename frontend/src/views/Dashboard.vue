<script setup>
import ControlPanel from '../components/ControlPanel.vue'; // Ajusta la ruta
import WeatherBar from '@/components/WeatherBar.vue';
</script>

<template>
    <div class="dashboard">
      <WeatherBar city="panama"/>
      <ControlPanel />
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
  