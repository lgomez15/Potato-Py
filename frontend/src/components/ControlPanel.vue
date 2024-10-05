<template>
  <div class="control-panel">
    <h1 class="panel-title">Control Panel</h1>

    <div class="info-cards">
      <div class="info-card">
        <h2>Velocidad del Viento</h2>
        <p>{{ weatherData.windSpeed }} km/h</p>
      </div>

      <div class="info-card">
        <h2>Dirección del Viento</h2>
        <p>{{ weatherData.windDirection }}°</p>
      </div>

      <div class="info-card">
        <h2>Ráfagas de Viento</h2>
        <p>{{ weatherData.windGusts }} km/h</p>
      </div>

      <div class="info-card">
        <h2>Precipitación 1h</h2>
        <p>{{ weatherData.precip1h }} mm</p>
      </div>

      <div class="info-card">
        <h2>Precipitación 24h</h2>
        <p>{{ weatherData.precip24h }} mm</p>
      </div>

      <div class="info-card">
        <h2>Temperatura</h2>
        <p>{{ weatherData.temperature }}°C</p>
      </div>
    </div>

    <div class="humidity-monitor" :class="humidityClass">
      <h2>Humedad del Suelo</h2>
      <p v-if="loading">Cargando...</p>
      <p v-else-if="error">{{ error }}</p>
      <p v-else>Humedad actual: {{ humidity }}%</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps } from 'vue';

// Definición de props
const props = defineProps({
  datetime: {
    type: String,
    required: true
  },
  latitude: {
    type: Number,
    required: true
  },
  longitude: {
    type: Number,
    required: true
  }
});

// Datos de la información del clima
const weatherData = ref({
  windSpeed: null,
  windDirection: null,
  windGusts: null,
  precip1h: null,
  precip24h: null,
  temperature: null,
});

// Datos de la humedad del suelo
const humidity = ref(null);
const loading = ref(true);
const error = ref(null);

// Clase para el monitor de humedad
const humidityClass = computed(() => {
  if (humidity.value === null) return "";
  if (humidity.value < 30) {
    return "low"; // Rojo
  } else if (humidity.value < 60) {
    return "medium"; // Amarillo
  } else {
    return "high"; // Verde
  }
});

// Función para obtener los datos del clima
const fetchWeatherData = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/weather/${props.datetime}/${props.latitude},${props.longitude}`);
    if (!response.ok) {
      throw new Error("Error al obtener datos del clima");
    }
    const data = await response.json();

    // Asignar los valores de la respuesta a weatherData
    weatherData.value.windSpeed = data.data.find(item => item.parameter === 'wind_speed_10m:kmh').coordinates[0].dates[0].value;
    weatherData.value.windDirection = data.data.find(item => item.parameter === 'wind_dir_10m:d').coordinates[0].dates[0].value;
    weatherData.value.windGusts = data.data.find(item => item.parameter === 'wind_gusts_10m_1h:kmh').coordinates[0].dates[0].value;
    weatherData.value.precip1h = data.data.find(item => item.parameter === 'precip_1h:mm').coordinates[0].dates[0].value;
    weatherData.value.precip24h = data.data.find(item => item.parameter === 'precip_24h:mm').coordinates[0].dates[0].value;
    weatherData.value.temperature = data.data.find(item => item.parameter === 't_2m:C').coordinates[0].dates[0].value;

  } catch (err) {
    console.error("Error al obtener datos del clima:", err);
    error.value = "No se pudo cargar los datos del clima.";
  }
};

// Función para obtener la humedad
const fetchHumidity = async () => {
  try {
    const response = await fetch("http://localhost:8000/humidity");
    if (!response.ok) {
      throw new Error("Error al obtener datos de humedad");
    }
    const data = await response.json();
    humidity.value = data.humidity;
  } catch (err) {
    console.error("Error al obtener la humedad:", err);
    error.value = "No se pudo cargar la humedad.";
  } finally {
    loading.value = false;
  }
};

// Llamar a las funciones en el montaje del componente
onMounted(() => {
  fetchWeatherData();
  fetchHumidity();
  setInterval(fetchHumidity, 10000); // Actualizar cada 10 segundos
});
</script>

<style scoped>
.control-panel {
  padding: 20px;
  background-color: white;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 20px auto;
  border-radius: 8px; /* Bordes menos redondeados */
}

.panel-title {
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.info-cards {
  display: flex; /* Cambiado de grid a flex */
  flex-wrap: wrap; /* Permitir que se envuelvan las tarjetas */
  justify-content: space-between; /* Espacio entre tarjetas */
  gap: 20px;
}

.info-card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px; /* Bordes menos redondeados */
  padding: 20px;
  text-align: center;
  width: calc(20% - 20px); /* Tamaño ajustado para ser rectangular */
  min-width: 200px; /* Ancho mínimo para cada tarjeta */
  transition: box-shadow 0.3s ease;
}

.info-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.humidity-monitor {
  padding: 20px;
  text-align: center;
  border-radius: 5px; /* Bordes menos redondeados */
  border: 1px solid #ddd;
  margin-top: 20px; /* Separar de la sección de clima */
}

.low {
  background-color: #ffcccc; /* Rojo claro */
}

.medium {
  background-color: #ffffcc; /* Amarillo claro */
}

.high {
  background-color: #ccffcc; /* Verde claro */
}

h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: #555;
}

p {
  font-size: 1.2em;
  margin: 0;
  color: #111;
}
</style>
