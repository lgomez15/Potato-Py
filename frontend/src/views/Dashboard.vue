<template>
    <div class="dashboard">
      <ControlPanel />
    </div>
  </template>
  
  <script setup>
  import ControlPanel from '../components/ControlPanel.vue'; // Ajusta la ruta
  </script>
  
  <style scoped>
  .dashboard {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #f2f2f2; /* Color de fondo del panel */
  }
  </style>
  