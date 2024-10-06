<template>
  <div class="control-panel">
    <h1 class="panel-title">Panel de Control</h1>

    <div class="info-cards">
      <div class="info-card">
        <h2>Velocidad del Viento</h2>
        <p>{{ weatherData.windSpeed !== null ? weatherData.windSpeed + ' km/h' : '---' }}</p>
      </div>

      <div class="info-card">
        <h2>Dirección del Viento</h2>
        <p>{{ weatherData.windDirection !== null ? weatherData.windDirection + '°' : '---' }}</p>
      </div>

      <div class="info-card">
        <h2>Ráfagas de Viento</h2>
        <p>{{ weatherData.windGusts !== null ? weatherData.windGusts + ' km/h' : '---' }}</p>
      </div>

      <div class="info-card">
        <h2>Precipitación 1h</h2>
        <p>{{ weatherData.precip1h !== null ? weatherData.precip1h + ' mm' : '---' }}</p>
      </div>

      <div class="info-card">
        <h2>Precipitación 24h</h2>
        <p>{{ weatherData.precip24h !== null ? weatherData.precip24h + ' mm' : '---' }}</p>
      </div>

      <div class="info-card">
        <h2>Temperatura</h2>
        <p>{{ weatherData.temperature !== null ? weatherData.temperature + '°C' : '---' }}</p>
      </div>
    </div>

    <div class="humidity-monitor" :class="humidityClass">
      <h2>Humedad del Suelo</h2>
      <p v-if="loading">Cargando...</p>
      <p v-else-if="error">{{ error }}</p>
      <p v-else>Humedad actual: {{ humidity !== null ? humidity + '%' : '---' }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps, watch } from 'vue';

const props = defineProps({
  datetime: {
    type: String,
    required: true
  },
  latitude: {
    type: Number,
    required: false
  },
  longitude: {
    type: Number,
    required: false
  }
});

const weatherData = ref({
  windSpeed: null,
  windDirection: null,
  windGusts: null,
  precip1h: null,
  precip24h: null,
  temperature: null,
});

const humidity = ref(null);
const loading = ref(true);
const error = ref(null);

const humidityClass = computed(() => {
  if (humidity.value === null) return "";
  if (humidity.value < 30) return "low";
  else if (humidity.value < 60) return "medium";
  else return "high";
});

const fetchWeatherData = async () => {
  if (!props.latitude || !props.longitude) return;

  try {
    const response = await fetch(`http://127.0.0.1:8000/weather/${props.datetime}/${props.latitude},${props.longitude}`);
    if (!response.ok) throw new Error("Error al obtener datos del clima");
    const data = await response.json();

    weatherData.value.windSpeed = data.data.find(item => item.parameter === 'wind_speed_10m:kmh')?.coordinates[0]?.dates[0]?.value || null;
    weatherData.value.windDirection = data.data.find(item => item.parameter === 'wind_dir_10m:d')?.coordinates[0]?.dates[0]?.value || null;
    weatherData.value.windGusts = data.data.find(item => item.parameter === 'wind_gusts_10m_1h:kmh')?.coordinates[0]?.dates[0]?.value || null;
    weatherData.value.precip1h = data.data.find(item => item.parameter === 'precip_1h:mm')?.coordinates[0]?.dates[0]?.value || null;
    weatherData.value.precip24h = data.data.find(item => item.parameter === 'precip_24h:mm')?.coordinates[0]?.dates[0]?.value || null;
    weatherData.value.temperature = data.data.find(item => item.parameter === 't_2m:C')?.coordinates[0]?.dates[0]?.value || null;

  } catch (err) {
    console.error("Error al obtener datos del clima:", err);
    error.value = "No se pudo cargar los datos del clima.";
  }
};

const fetchHumidity = async () => {
  try {
    const response = await fetch("http://localhost:8000/humidity");
    if (!response.ok) throw new Error("Error al obtener datos de humedad");
    const data = await response.json();
    humidity.value = data.humidity;
  } catch (err) {
    console.error("Error al obtener la humedad:", err);
    error.value = "No se pudo cargar la humedad.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchWeatherData();
  fetchHumidity();
  setInterval(fetchHumidity, 1000); // Actualizar cada 10 segundos
});

watch(() => [props.latitude, props.longitude], () => {
  fetchWeatherData();
});
</script>
<style scoped>
.control-panel {
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;
  background-color: #f0f4f8;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.panel-title {
  text-align: center;
  font-size: 2.5rem;
  color: #34495e;
  margin-bottom: 25px;
  letter-spacing: 1.2px;
}

.info-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.info-card {
  background: linear-gradient(135deg, #e9eff5, #f6f9fc);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  flex: 1 1 calc(33.33% - 20px); /* Tres columnas */
  min-width: 200px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.info-card h2 {
  font-size: 1.75rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.info-card p {
  font-size: 1.2rem;
  color: #34495e;
}

.humidity-monitor {
  padding: 25px;
  margin-top: 30px;
  background-color: #eef2f7;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.low {
  background-color: #ffcccc;
}

.medium {
  background-color: #ffffcc;
}

.high {
  background-color: #ccffcc;
}

h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #555;
}

p {
  font-size: 1.2rem;
  color: #111;
}

/* Media queries para hacer el diseño responsive */
@media (max-width: 768px) {
  .info-cards {
    flex-direction: column;
    gap: 15px;
  }

  .info-card {
    width: 100%;
  }
}

@media (min-width: 1200px) {
  .info-card {
    flex: 1 1 calc(25% - 20px); /* Cuatro columnas para pantallas grandes */
  }
}
</style>
