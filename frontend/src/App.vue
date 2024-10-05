<script setup>
  import { RouterView } from 'vue-router';
  import InformationPanel from './components/InformationPanel.vue';

</script>

<template>
  <div>
    <InformationPanel/>
    <RouterView/>
  </div>
</template>