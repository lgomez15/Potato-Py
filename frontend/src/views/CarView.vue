<script setup>
import { useRoute, useRouter, RouterView } from 'vue-router';
import cars from '../data/cars.json';

const route = useRoute();
const car = cars.find(car => car.id === Number(route.params.id));

const router = useRouter();

</script>

<template>
    <div v-if="car">
        <h1>Car</h1>
        <p>Welcome to your car page with Vue.js app!</p>
        <p>{{ car.name }}</p>
        <p>{{ car.price }}</p>
        <!-- This RouterView is to render the child route -->
         <button @click="router.push(`/car/${car.id}/contact`)">Contact</button>
        <RouterView />
    </div>
    <div v-else>
        <p>Car not found</p>
    </div>
</template>

<style scoped>
    h1 {
        color: #35495e;
    }
    p {
        color: #41b883;
    }
    button {
        background-color: #41b883;
        color: #fff;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    button:hover {
        background-color: #35495e;
    }
</style>