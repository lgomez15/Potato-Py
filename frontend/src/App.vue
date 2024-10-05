<script setup>
  import { RouterView } from 'vue-router';
  import InformationPanel from './components/InformationPanel.vue';
  import HumidityMonitor from './components/HumidityMonitor.vue';
import WeatherVar from './components/weatherVar.vue';

</script>

<template>
  <div>
    <WeatherVar city="Madrid"/>
    <InformationPanel/>
    <HumidityMonitor/>
    <RouterView/>
  </div>
</template>