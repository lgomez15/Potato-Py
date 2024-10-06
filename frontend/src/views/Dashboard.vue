<!-- Dashboard.vue -->
<template>
  <div class="dashboard">
    <div class="search-section">
      <input 
        type="text" 
        v-model="cityInput" 
        @input="fetchCities" 
        placeholder="Escribe el nombre de la ciudad" 
        class="city-input"
      />
      
      <!-- Lista de sugerencias -->
      <ul v-if="filteredCities.length > 0" class="suggestions">
        <li 
          v-for="(city, index) in filteredCities" 
          :key="index" 
          @click="selectCity(city)" 
          class="suggestion-item"
        >
          {{ city.name }}, {{ city.country }}
        </li>
      </ul>

      <!-- Botón de búsqueda -->
      <button @click="fetchCoordinates" class="search-button">Buscar</button>
    </div>

    <!-- Mensaje de error -->
    <p v-if="error" class="error-message">{{ error }}</p>

    <!-- Barra del tiempo -->
    <div v-if="latitude !== null && longitude !== null">
      <WeatherBar
        :datetime="datetime"
        :latitude="latitude"
        :longitude="longitude"
        :city="selectedCity"
      />
    </div>

    <!-- Panel de control -->
    <div v-if="latitude !== null && longitude !== null">
      <ControlPanel
        :datetime="datetime"
        :latitude="latitude"
        :longitude="longitude"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ControlPanel from '../components/ControlPanel.vue';
import WeatherBar from '@/components/WeatherBar.vue';

const apiKey = 'd2736c1d75667857ddcc39a3dc4651c3'; // Asegúrate de reemplazar con tu API Key
const datetime = new Date().toISOString();
const cityInput = ref('');
const selectedCity = ref('');
const filteredCities = ref([]); 
const latitude = ref(null);
const longitude = ref(null);
const error = ref(null);

// Función para buscar ciudades
const fetchCities = async () => {
  if (!cityInput.value) {
    filteredCities.value = [];
    return;
  }

  const geocodingUrl = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(cityInput.value)}&limit=5&appid=${apiKey}`;

  try {
    const response = await fetch(geocodingUrl);
    if (!response.ok) throw new Error('Error en la respuesta de la API');
    const data = await response.json();
    filteredCities.value = data;
  } catch (error) {
    console.error('Error al buscar ciudades:', error);
  }
};

// Seleccionar ciudad
const selectCity = (city) => {
  selectedCity.value = city.name;
  cityInput.value = `${city.name}, ${city.country}`;
  filteredCities.value = [];
};

// Función para obtener las coordenadas de la ciudad seleccionada
const fetchCoordinates = async () => {
  if (!selectedCity.value) {
    error.value = 'Por favor, introduce una ciudad.';
    return;
  }

  const geocodingUrl = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(selectedCity.value)}&limit=1&appid=${apiKey}`;

  try {
    const response = await fetch(geocodingUrl);
    if (!response.ok) throw new Error('Error en la respuesta de la API');
    const data = await response.json();
    if (data.length > 0) {
      latitude.value = data[0].lat;
      longitude.value = data[0].lon;
      error.value = null;
    } else {
      error.value = 'No se encontraron coordenadas para la ciudad ingresada.';
      latitude.value = null;
      longitude.value = null;
    }
  } catch (error) {
    error.value = 'Error al obtener coordenadas.';
    console.error(error);
  }
};

onMounted(() => {
  selectedCity.value = 'Salamanca';
  cityInput.value = 'Salamanca, ES';
  fetchCoordinates();
});
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.city-input {
  width: 100%;
  max-width: 500px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-bottom: 10px;
}

.suggestions {
  width: 100%;
  max-width: 500px;
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ddd;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 10px;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f0f0f0;
}

.search-button {
  background-color: var(--primary-color);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  margin-top: 10px;
}

.search-button:hover {
  background-color: var(--secondary-color);
}

.error-message {
  color: #e74c3c;
  text-align: center;
  margin-top: 10px;
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  .search-section {
    width: 100%;
  }
}
</style>
