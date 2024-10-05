<script setup>
import { RouterLink } from 'vue-router';

</script>

<template>
  <nav>
    <router-link active-class="active" to="/">Home</router-link>
    <router-link active-class="active" to="/about">About</router-link>
  </nav>
</template>


<style scoped>
    .active {
        font-weight: bold;
        color: red;
    }

    nav {
        background-color: #35495e;
        padding: 10px;
    }

    a {
        color: #fff;
        text-decoration: none;
        margin-right: 10px;
    }

    
</style>