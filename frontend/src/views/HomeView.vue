<script setup>
    import { ref } from 'vue';
    import { RouterLink } from 'vue-router';
    import cars from '../data/cars.json';
</script>


<template>
    <div>
        <h1>Home</h1>
        <p>Welcome to your home page with Vue.js app!</p>
        <div class="cars">
            <router-link v-for="car in cars" :key="car.id" :to="'/car/' + car.id">
                {{ car.name }}
            </router-link>
        </div>
    </div>
</template>

<style scoped>
    .cars {
        display: flex;
        flex-wrap: wrap;
    }
    .cars a {
        margin: 10px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        text-decoration: none;
        color: #333;
    }

    .cars a:hover {
        background-color: #f9f9f9;
    }
</style>