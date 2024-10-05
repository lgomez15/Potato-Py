<template>
  <div class="weather-week">
    <h2>Pronóstico de la Semana en {{ city }}</h2>
    
    <!-- Mostrar el pronóstico semanal -->
    <div v-if="weeklyWeather.length" class="weekly-weather-container">
      <div v-for="day in weeklyWeather" :key="day.date" class="weather-day">
        <p class="date">{{ formatDate(day.date) }}</p>
        <!-- Ícono del clima -->
        <i :class="['wi', getWeatherIcon(day)]" class="weather-icon"></i>
        <p class="temperature">Máx: {{ day.temp_max }}°C / Mín: {{ day.temp_min }}°C</p>
        <p class="precipitation">Precipitación: {{ day.precipitation }} mm</p>
      </div>
    </div>
    
    <!-- Manejo de Errores -->
    <div v-else-if="error" class="error-message">
      <p>Error: {{ error }}</p>
    </div>
    
    <!-- Estado de Carga -->
    <div v-else class="loading-message">
      <p>Cargando pronóstico de la semana...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import 'weather-icons/css/weather-icons.css';

export default {
  name: 'WeatherWeek',
  props: {
    city: {
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
    },
    datetime: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      weeklyWeather: [],
      error: null
    };
  },
  watch: {
    city(newCity, oldCity) {
      if (newCity !== oldCity) {
        this.fetchWeeklyWeather();
      }
    },
    latitude(newLat, oldLat) {
      if (newLat !== oldLat) {
        this.fetchWeeklyWeather();
      }
    },
    longitude(newLon, oldLon) {
      if (newLon !== oldLon) {
        this.fetchWeeklyWeather();
      }
    },
    datetime(newDatetime, oldDatetime) {
      if (newDatetime !== oldDatetime) {
        this.fetchWeeklyWeather();
      }
    }
  },
  mounted() {
    this.fetchWeeklyWeather();
  },
  methods: {
    formatDate(dateStr) {
      const options = { weekday: 'short', day: 'numeric', month: 'short' };
      const date = new Date(dateStr);
      return date.toLocaleDateString(undefined, options);
    },
    
    getWeatherIcon(day) {
      const { temp_max, temp_min, precipitation } = day;
      
      if (precipitation > 10) {
        return 'wi-rain';
      } else if (precipitation > 0) {
        if (temp_min <= 0) {
          return 'wi-snow';
        }
        return 'wi-showers';
      } else {
        if (temp_max >= 25) {
          return 'wi-day-sunny';
        } else if (temp_max >= 20 && temp_max < 25) {
          return 'wi-day-cloudy';
        } else {
          return 'wi-day-sunny';
        }
      }
    },
    
    async fetchWeeklyWeather() {
      this.weeklyWeather = [];
      this.error = null;
      
      try {
        const apiUrl = `http://127.0.0.1:8000/weather/week/${encodeURIComponent(this.datetime)}/${this.latitude},${this.longitude}`;
        const response = await axios.get(apiUrl);
        
        if (!response.data || !Array.isArray(response.data.data)) {
          throw new Error('Estructura de respuesta inesperada');
        }
        
        const tempMaxParam = response.data.data.find(param => param.parameter === 't_max_2m_24h:C');
        const tempMinParam = response.data.data.find(param => param.parameter === 't_min_2m_24h:C');
        const precipitationParam = response.data.data.find(param => param.parameter === 'precip_24h:mm');
        
        if (!tempMaxParam || !tempMinParam || !precipitationParam) {
          throw new Error('Parámetros de temperatura o precipitación no encontrados en la respuesta');
        }
        
        const datesMax = tempMaxParam.coordinates[0].dates;
        const datesMin = tempMinParam.coordinates[0].dates;
        const datesPrecip = precipitationParam.coordinates[0].dates;
        
        if (datesMax.length !== datesMin.length || datesMax.length !== datesPrecip.length) {
          throw new Error('Las temperaturas y precipitaciones no coinciden en cantidad de días');
        }
        
        const weeklyData = datesMax.slice(1).map((dayMax, index) => {
          const dayMin = datesMin[index + 1];
          const dayPrecip = datesPrecip[index + 1];
          return {
            date: dayMax.date,
            temp_max: dayMax.value,
            temp_min: dayMin.value,
            precipitation: dayPrecip.value
          };
        });
        
        this.weeklyWeather = weeklyData;
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Error al obtener el pronóstico semanal.';
      }
    }
  }
};
</script>

<style scoped>
.weather-week {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem;
  background: linear-gradient(135deg, #f0f4f8, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  margin: 0 auto 2rem auto;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.weekly-weather-container {
  display: flex;
  flex-wrap: nowrap; /* Alinea las tarjetas en una sola línea */
  overflow-x: auto; /* Permite el desplazamiento horizontal */
  gap: 15px;
}

.weather-day {
  background: linear-gradient(135deg, #e9eff5, #f6f9fc);
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  min-width: 150px; /* Asegura que las tarjetas mantengan un tamaño adecuado */
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  flex-shrink: 0;
}

.weather-day:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.date {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #555;
}

.weather-icon {
  font-size: 2rem;
  color: #2980b9;
  margin-bottom: 0.5rem;
}

.temperature, .precipitation {
  margin: 0.3rem 0;
  color: #333;
}

.precipitation {
  color: #1976d2;
}

.error-message, .loading-message {
  text-align: center;
  margin-top: 2rem;
  color: #d32f2f;
  font-weight: bold;
}
</style>
