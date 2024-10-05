<template>
  <div class="weather-week">
    <h2>Pronóstico de la Semana en {{ city }}</h2>
    
    <!-- Mostrar el pronóstico semanal -->
    <div v-if="weeklyWeather.length" class="weekly-weather-container">
      <div v-for="day in weeklyWeather" :key="day.date" class="weather-day">
        <p class="date">{{ formatDate(day.date) }}</p>
        <!-- Ícono del clima -->
        <i :class="['wi', getWeatherIcon(day)]" class="weather-icon"></i>
        <p class="temperature">Máxima: {{ day.temp_max }} °C</p>
        <p class="temperature">Mínima: {{ day.temp_min }} °C</p>
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
import 'weather-icons/css/weather-icons.css'; // Asegúrate de haber instalado y configurado weather-icons

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
      weeklyWeather: [], // Array para almacenar los datos del pronóstico semanal
      error: null         // Manejo de errores
    };
  },
  watch: {
    /**
     * Observa cambios en las props 'city', 'latitude', 'longitude' y 'datetime' para actualizar el pronóstico semanal.
     */
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
    /**
     * Formatea una fecha en formato legible.
     * @param {String} dateStr - Fecha en formato ISO.
     * @returns {String} Fecha formateada.
     */
    formatDate(dateStr) {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      const date = new Date(dateStr);
      return date.toLocaleDateString(undefined, options);
    },
    
    /**
     * Determina el ícono del clima basado en las temperaturas máximas, mínimas y precipitación.
     * @param {Object} day - Objeto que contiene temp_max, temp_min y precipitation.
     * @returns {String} Clase de ícono de weather-icons.
     */
    getWeatherIcon(day) {
      const { temp_max, temp_min, precipitation } = day;
      
      // Lógica para determinar la condición climática basada en precipitación
      if (precipitation > 10) {
        return 'wi-rain'; // Lluvia intensa
      } else if (precipitation > 0) {
        if (temp_min <= 0) {
          return 'wi-snow'; // Nieve
        }
        return 'wi-showers'; // Lluvia ligera
      } else {
        // Lógica basada en la temperatura
        if (temp_max >= 25) {
          return 'wi-day-sunny'; // Soleado
        } else if (temp_max >= 20 && temp_max < 25) {
          return 'wi-day-cloudy'; // Nublado
        } else {
          return 'wi-day-sunny'; // Por defecto: Soleado
        }
      }
    },
    
    /**
     * Obtiene el pronóstico del tiempo para la semana desde tu API.
     */
    async fetchWeeklyWeather() {
      this.weeklyWeather = [];
      this.error = null;
      
      try {
        // Construir la URL de tu API para el pronóstico semanal
        const apiUrl = `http://127.0.0.1:8000/weather/week/${encodeURIComponent(this.datetime)}/${this.latitude},${this.longitude}`;
        
        // Realizar la petición a tu API
        const response = await axios.get(apiUrl);
        console.log("response (Weekly)", response);
        
        // Verificar si la respuesta tiene la estructura esperada
        if (!response.data || !Array.isArray(response.data.data)) {
          throw new Error('Estructura de respuesta inesperada');
        }
        
        // Extraer los datos necesarios
        const tempMaxParam = response.data.data.find(param => param.parameter === 't_max_2m_24h:C');
        const tempMinParam = response.data.data.find(param => param.parameter === 't_min_2m_24h:C');
        const precipitationParam = response.data.data.find(param => param.parameter === 'precip_24h:mm');
        
        if (!tempMaxParam || !tempMinParam || !precipitationParam) {
          throw new Error('Parámetros de temperatura o precipitación no encontrados en la respuesta');
        }
        
        const datesMax = tempMaxParam.coordinates[0].dates;
        const datesMin = tempMinParam.coordinates[0].dates;
        const datesPrecip = precipitationParam.coordinates[0].dates;
        
        // Asegurar que todos los arrays tengan la misma longitud
        if (datesMax.length !== datesMin.length || datesMax.length !== datesPrecip.length) {
          throw new Error('Las temperaturas y precipitaciones no coinciden en cantidad de días');
        }
        
        // Construir el array de pronóstico semanal, omitiendo el primer día si es el día actual
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
        
        // Asignar los datos transformados a weeklyWeather
        this.weeklyWeather = weeklyData;
        
        // Imprimir las temperaturas y precipitaciones en la consola para verificación
        console.log("Pronóstico Semanal:", this.weeklyWeather);
        
      } catch (error) {
        console.error('Error obteniendo pronóstico semanal', error);
        this.error = error.response?.data?.detail || error.message || 'Ocurrió un error al obtener el pronóstico semanal.';
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
  max-width: 800px;
  margin: 0 auto 2rem auto;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1rem;
}

.weekly-weather-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.weather-day {
  background: linear-gradient(135deg, #e9eff5, #f6f9fc);
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0.5rem;
  width: 200px;
  text-align: center;
}

.date {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #555;
}

.weather-icon {
  font-size: 2rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.temperature, .precipitation {
  margin: 0.3rem 0;
  color: #333;
}

.precipitation {
  color: #1976d2; /* Color azul para destacar la precipitación */
}

.error-message, .loading-message {
  text-align: center;
  margin-top: 2rem;
  color: #d32f2f;
  font-weight: bold;
}

@media (max-width: 600px) {
  .weather-day {
    width: 100%;
    margin: 0.5rem 0;
  }
}
</style>
