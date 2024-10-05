<template>
  <div class="dashboard">
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
    <button @click="fetchCoordinates" class="search-button">Buscar Coordenadas</button>

    <!-- Mensaje de error -->
    <p v-if="error" class="error-message">{{ error }}</p>

    <!-- Barra del tiempo -->
    <WeatherBar
      :datetime="datetime"
      :latitude="latitude"
      :longitude="longitude"
      :city="selectedCity"
    />

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

const apiKey = 'd2736c1d75667857ddcc39a3dc4651c3';
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
  fetchCoordinates();
});
</script>

<style scoped>
.dashboard {
  display: block;
  width: 100%;
  max-width: 1200px; /* Establecer un límite de ancho */
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

h2 {
  font-size: 1.8rem;
  color: #34495e;
  margin-bottom: 20px;
}

.city-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s ease;
}

.city-input:focus {
  border-color: #3498db;
  outline: none;
}

.suggestions {
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 200px; /* Altura máxima para el scroll */
  overflow-y: auto;
}

.suggestion-item {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.suggestion-item:hover {
  background-color: #ecf0f1;
}

.search-button {
  background-color: #3498db;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  font-size: 1em;
  width: 100%;
}

.search-button:hover {
  background-color: #2980b9;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.error-message {
  color: #e74c3c;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  h2 {
    font-size: 1.5rem;
  }

  .search-button {
    font-size: 0.9em;
  }
}
</style>
