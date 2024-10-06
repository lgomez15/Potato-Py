<template>
  <div class="control-panel">
    <h1 class="panel-title">Panel de Control</h1>

    <div class="info-cards">
      <div class="info-card">
        <i class="fas fa-wind icon"></i>
        <h2>Velocidad del Viento</h2>
        <p>{{ weatherData.windSpeed !== null ? weatherData.windSpeed + ' km/h' : '---' }}</p>
      </div>

      <div class="info-card">
        <i class="fas fa-compass icon"></i>
        <h2>Dirección del Viento</h2>
        <p>{{ weatherData.windDirection !== null ? weatherData.windDirection + '°' : '---' }}</p>
      </div>

      <div class="info-card">
        <i class="fas fa-wind icon"></i>
        <h2>Ráfagas de Viento</h2>
        <p>{{ weatherData.windGusts !== null ? weatherData.windGusts + ' km/h' : '---' }}</p>
      </div>

      <div class="info-card">
        <i class="fas fa-cloud-rain icon"></i>
        <h2>Precipitación 1h</h2>
        <p>{{ weatherData.precip1h !== null ? weatherData.precip1h + ' mm' : '---' }}</p>
      </div>

      <div class="info-card">
        <i class="fas fa-cloud-showers-heavy icon"></i>
        <h2>Precipitación 24h</h2>
        <p>{{ weatherData.precip24h !== null ? weatherData.precip24h + ' mm' : '---' }}</p>
      </div>

      <div class="info-card">
        <i class="fas fa-thermometer-half icon"></i>
        <h2>Temperatura</h2>
        <p>{{ weatherData.temperature !== null ? weatherData.temperature + '°C' : '---' }}</p>
      </div>
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
    required: true
  },
  longitude: {
    type: Number,
    required: true
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
    const response = await fetch(`http://35.187.77.55:8000/weather/${props.datetime}/${props.latitude},${props.longitude}`);
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
    const response = await fetch("http://35.187.77.55:8000/humidity");
    console.log(response);
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
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.panel-title {
  text-align: center;
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 30px;
}

.info-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.info-card {
  background: linear-gradient(135deg, #a5d6a7, #e8f5e9);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  flex: 1 1 calc(33% - 40px);
  max-width: calc(33% - 40px);
  min-width: 250px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.info-card h2 {
  font-size: 1.5rem;
  color: var(--text-color);
  margin-bottom: 10px;
}

.info-card p {
  font-size: 1.2rem;
  color: var(--text-color);
}

.icon {
  font-size: 2rem;
  color: var(--secondary-color);
  margin-bottom: 10px;
}

.humidity-monitor {
  padding: 25px;
  margin-top: 30px;
  background-color: #fffde7;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.low {
  background-color: #ffccbc;
}

.medium {
  background-color: #fff9c4;
}

.high {
  background-color: #c8e6c9;
}

.humidity-monitor h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.humidity-monitor p {
  font-size: 1.2rem;
  color: var(--text-color);
}

/* Responsividad */
@media (max-width: 768px) {
  .info-card {
    flex: 1 1 100%;
    max-width: 100%;
  }
}
</style>
