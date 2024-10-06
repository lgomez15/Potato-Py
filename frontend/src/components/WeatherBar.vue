<template>
  <div class="weather-bar">
    <h2>Pronóstico Semanal en {{ city }}</h2>
    <div class="weather-container">
      <!-- Botón de desplazamiento a la izquierda -->
      <button class="scroll-button left" @click="scrollLeft">
        <i class="fas fa-chevron-left"></i>
      </button>

      <!-- Contenedor deslizable del pronóstico -->
      <div class="weather-slider" ref="weatherSlider">
        <div v-for="day in weeklyWeather" :key="day.date" class="weather-day">
          <p class="date">{{ formatDate(day.date) }}</p>
          <!-- Ícono del clima -->
          <i :class="['wi', getWeatherIcon(day)]" class="weather-icon"></i>
          <p class="temperature">Máx: {{ day.temp_max }}°C</p>
          <p class="temperature">Mín: {{ day.temp_min }}°C</p>
          <p class="precipitation">Precipitación: {{ day.precipitation }} mm</p>
        </div>
      </div>

      <!-- Botón de desplazamiento a la derecha -->
      <button class="scroll-button right" @click="scrollRight">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>

    <!-- Manejo de Errores -->
    <div v-if="error" class="error-message">
      <p>Error: {{ error }}</p>
    </div>

    <!-- Estado de Carga -->
    <div v-else-if="!weeklyWeather.length" class="loading-message">
      <p>Cargando pronóstico de la semana...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import 'weather-icons/css/weather-icons.css';
import '@fortawesome/fontawesome-free/css/all.css';

export default {
  name: 'WeatherBar',
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
          return 'wi-cloud';
        }
      }
    },

    async fetchWeeklyWeather() {
      if (this.latitude === null || this.longitude === null) {
        this.error = 'Coordenadas no disponibles.';
        return;
      }

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
    },

    scrollLeft() {
      this.$refs.weatherSlider.scrollBy({
        top: 0,
        left: -200,
        behavior: 'smooth'
      });
    },

    scrollRight() {
      this.$refs.weatherSlider.scrollBy({
        top: 0,
        left: 200,
        behavior: 'smooth'
      });
    }
  }
};
</script>

<style scoped>
.weather-bar {
  font-family: 'Poppins', sans-serif;
  padding: 1rem;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  margin: 20px auto;
  position: relative;
}

.weather-bar h2 {
  text-align: center;
  color: var(--text-color);
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.weather-container {
  display: flex;
  align-items: center;
  position: relative;
}

.weather-slider {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  -ms-overflow-style: none; /* Para Internet Explorer y Edge */
  scrollbar-width: none; /* Para Firefox */
  width: 100%;
}

.weather-slider::-webkit-scrollbar {
  display: none; /* Oculta la barra de desplazamiento en Chrome, Safari y Opera */
}

.weather-day {
  background: linear-gradient(135deg, #a5d6a7, #e8f5e9);
  padding: 1rem;
  border-radius: 8px;
  min-width: 150px;
  margin: 0 10px;
  text-align: center;
  flex-shrink: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.weather-day:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.date {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.weather-icon {
  font-size: 2.5rem;
  color: #ffb300;
  margin-bottom: 0.5rem;
}

.temperature, .precipitation {
  margin: 0.3rem 0;
  color: var(--text-color);
}

.precipitation {
  color: #0288d1;
}

.scroll-button {
  background-color: rgba(76, 175, 80, 0.8);
  border: none;
  color: #fff;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

.scroll-button.left {
  left: -10px;
}

.scroll-button.right {
  right: -10px;
}

.scroll-button:hover {
  background-color: rgba(56, 142, 60, 0.8);
}

.scroll-button i {
  font-size: 1.2rem;
}

.error-message, .loading-message {
  text-align: center;
  margin-top: 2rem;
  color: #d32f2f;
  font-weight: bold;
}

/* Responsividad */
@media (max-width: 768px) {
  .weather-bar h2 {
    font-size: 1.5rem;
  }

  .weather-day {
    min-width: 120px;
    padding: 0.8rem;
  }

  .scroll-button {
    display: none; /* Oculta los botones en pantallas pequeñas */
  }
}
</style>
