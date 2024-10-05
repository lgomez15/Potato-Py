<script setup>
  import { RouterView } from 'vue-router';
  import Nav from './components/Navbar.vue';
</script>

<template>
  <div>
    <Nav></Nav>
    <RouterView/>
  </div>
</template>