<template>
  <div class="dashboard">
    <input 
      type="text" 
      v-model="cityInput" 
      @input="fetchCities" 
      placeholder="Escribe el nombre de la ciudad" 
    />
    <ul v-if="filteredCities.length > 0" class="suggestions">
      <li 
        v-for="(city, index) in filteredCities" 
        :key="index" 
        @click="selectCity(city)"
      >
        {{ city.name }}, {{ city.country }}
      </li>
    </ul>
    <button @click="fetchCoordinates">Buscar Coordenadas</button>
    
    <p v-if="error" class="error">{{ error }}</p>

    <WeatherBar
      :datetime="datetime" 
      :latitude="latitude" 
      :longitude="longitude" 
      :city="selectedCity"
    />
    
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
const filteredCities = ref([]); // Almacena las ciudades filtradas
const latitude = ref(null);
const longitude = ref(null);
const error = ref(null); 

// Función para buscar ciudades
const fetchCities = async () => {
  if (!cityInput.value) {
    filteredCities.value = []; // Limpiar ciudades si no hay texto
    return;
  }

  const geocodingUrl = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(cityInput.value)}&limit=5&appid=${apiKey}`;

  try {
    const response = await fetch(geocodingUrl);
    if (!response.ok) {
      throw new Error('Error en la respuesta de la API');
    }
    const data = await response.json();
    filteredCities.value = data; // Asignar datos filtrados
  } catch (error) {
    console.error('Error al buscar ciudades:', error);
  }
};

// Seleccionar ciudad
const selectCity = (city) => {
  selectedCity.value = city.name;
  cityInput.value = `${city.name}, ${city.country}`; // Actualiza el input con la ciudad seleccionada
  filteredCities.value = []; // Limpiar las sugerencias
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
    if (!response.ok) {
      throw new Error('Error en la respuesta de la API');
    }
    const data = await response.json();

    if (data.length > 0) {
      latitude.value = data[0].lat; 
      longitude.value = data[0].lon; 
      error.value = null; 

      console.log(`Coordenadas de ${selectedCity.value}:`, {
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
  padding: 20px;
}
input {
  width: 70%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.suggestions {
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.suggestions li {
  padding: 10px;
  cursor: pointer;
}
.suggestions li:hover {
  background-color: #f0f0f0;
}
button {
  padding: 10px;
  border: none;
  background-color: #007BFF; 
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
button:hover {
  background-color: #0056b3; 
}
</style>
