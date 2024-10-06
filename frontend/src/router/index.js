import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Dashboard from "../views/Dashboard.vue"; // Cambia la ruta a 'views'
import PerformanceView from "@/views/PerformanceView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: Dashboard
        },
        {
            path: "/dashboard", // Nueva ruta para el Dashboard
            name: "dashboard",
            component: Dashboard // Asocia el Dashboard al nombre de la ruta
        },
        {
            path: "/performance",
            name: "performance",
            component: PerformanceView
        }
    ]
});

export default router;
