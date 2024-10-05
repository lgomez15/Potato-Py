<script setup>
  import { RouterView } from 'vue-router';
  import InformationPanel from './components/InformationPanel.vue';
  import HumidityMonitor from './components/HumidityMonitor.vue';

</script>

<template>
  <div>
    <InformationPanel/>
    <HumidityMonitor/>
    <RouterView/>
  </div>
</template>