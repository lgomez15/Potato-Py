<template>
  <div class="dashboard">
    <input 
      type="text" 
      v-model="cityInput" 
      placeholder="Escribe el nombre de la ciudad"
    />
    <button @click="fetchCoordinates">Buscar Coordenadas</button>
    
    <!-- Mostrar mensajes de error si existen -->
    <p v-if="error" class="error">{{ error }}</p>
    
    <!-- Mostrar ControlPanel y WeatherWeek si las coordenadas están disponibles -->
    <div v-if="latitude !== null && longitude !== null">
      <ControlPanel 
        :datetime="datetime" 
        :latitude="latitude" 
        :longitude="longitude" 
      />
      
      <!-- Pasar las coordenadas y datetime a WeatherWeek -->
      <WeatherBar
        :datetime="datetime" 
        :latitude="latitude" 
        :longitude="longitude" 
        :city="cityInput"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ControlPanel from '../components/ControlPanel.vue'; // Ajusta la ruta
import WeatherBar from '@/components/WeatherBar.vue';

const apiKey = 'd2736c1d75667857ddcc39a3dc4651c3'; // Tu clave de API de OpenWeatherMap
const datetime = new Date().toISOString(); // Fecha y hora actual
const cityInput = ref(''); // Campo de entrada para la ciudad
const latitude = ref(null);
const longitude = ref(null);
const error = ref(null); // Mensaje de error

// Función para obtener las coordenadas de la ciudad ingresada
const fetchCoordinates = async () => {
  if (!cityInput.value) {
    error.value = 'Por favor, introduce una ciudad.';
    return;
  }

  const geocodingUrl = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(cityInput.value)}&limit=1&appid=${apiKey}`;

  try {
    const response = await fetch(geocodingUrl);
    if (!response.ok) {
      throw new Error('Error en la respuesta de la API');
    }
    const data = await response.json();

    // Comprobar si se encontraron coordenadas
    if (data.length > 0) {
      latitude.value = data[0].lat; // Asignar latitud
      longitude.value = data[0].lon; // Asignar longitud
      error.value = null; // Limpiar mensaje de error

      // Imprimir coordenadas en consola para depuración
      console.log(`Coordenadas de ${cityInput.value}:`, {
        latitude: latitude.value,
        longitude: longitude.value,
      });
    } else {
      error.value = "No se encontraron coordenadas para la ciudad ingresada.";
      latitude.value = null;
      longitude.value = null;
    }
  } catch (error) {
    error.value = "Error al obtener coordenadas.";
    console.error(error); // Para depuración
  }
};

// Cargar las coordenadas de Salamanca al montar el componente
onMounted(() => {
  cityInput.value = 'Salamanca'; // Establecer Salamanca como valor predeterminado
  fetchCoordinates(); // Llamar a la función para obtener las coordenadas
});
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
input {
  width: 70%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
button {
  padding: 10px;
  border: none;
  background-color: #007BFF; /* Color azul */
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
button:hover {
  background-color: #0056b3; /* Color azul oscuro al pasar el ratón */
}
</style>
