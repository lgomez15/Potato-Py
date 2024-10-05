<template>
  <div class="weather-week">
    <h2>Pronóstico de la Semana en {{ city }}</h2>
    
    <!-- Mostrar el pronóstico semanal -->
    <div v-if="weeklyWeather.length" class="weekly-weather-container">
      <div v-for="day in weeklyWeather" :key="day.date" class="weather-day">
        <p class="date">{{ formatDate(day.date) }}</p>
        <p class="temperature">Temperatura Máxima: {{ day.temp_max }} °C</p>
        <p class="temperature">Temperatura Mínima: {{ day.temp_min }} °C</p>
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
  name: 'WeatherBar',
  props: {
    city: {
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
  mounted() {
    this.fetchWeeklyWeather(this.city);
  },
  watch: {
    /**
     * Observa cambios en la prop 'city' para actualizar el pronóstico semanal.
     */
    city(newCity, oldCity) {
      if (newCity !== oldCity) {
        this.fetchWeeklyWeather(newCity);
      }
    }
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
     * Obtiene las coordenadas (latitud y longitud) de una ciudad usando el endpoint de Geocodificación del backend.
     * @param {String} city - Nombre de la ciudad.
     * @returns {Object} Objeto con latitud y longitud.
     */
    async getCoordinates(city) {
      const apiKey = 'd2736c1d75667857ddcc39a3dc4651c3'; // Tu clave de API de OpenWeatherMap
      const geocodingUrl = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(city)}&limit=1&appid=${apiKey}`;
      
      try {
        const response = await axios.get(geocodingUrl);
        if (response.data && response.data.length > 0) {
          const { lat, lon } = response.data[0];
          console.log('Coordenadas:', { latitude: lat, longitude: lon });
          return { latitude: lat, longitude: lon };
        } else {
          throw new Error('No se encontraron coordenadas para la ciudad proporcionada.');
        }
      } catch (error) {
        console.error('Error obteniendo coordenadas', error);
        throw new Error('No se pudieron obtener las coordenadas de la ciudad.');
      }
    },
    
    /**
     * Obtiene el pronóstico del tiempo para la semana desde tu API.
     * @param {String} city - Nombre de la ciudad.
     */
    async fetchWeeklyWeather(city) {
      try {
        // Obtener las coordenadas de la ciudad
        const { latitude, longitude } = await this.getCoordinates(city);
        
        // Obtener la fecha y hora actual en formato ISO
        const currentDatetime = new Date().toISOString();
        
        // Construir la URL de tu API para el pronóstico semanal
        const apiUrl = `http://127.0.0.1:8000/weather/week/${encodeURIComponent(currentDatetime)}/${latitude},${longitude}`;
        
        // Realizar la petición a tu API
        const response = await axios.get(apiUrl);
        console.log("response (Weekly)", response);
        console.log("Temperaturas", response.data.data[0].p); 
        
        // Verificar si la respuesta tiene la estructura esperada
        if (!response.data || !Array.isArray(response.data.data)) {
          throw new Error('Estructura de respuesta inesperada');
        }
        
        // Suponiendo que tu API devuelve parámetros como 't_max_2m:C' y 't_min_2m:C' para cada día
        // Ajusta estos nombres según la estructura real de tu respuesta
        
        // Extraer los datos de temperatura máxima y mínima
        const tempMaxParam = response.data.data.find(param => param.parameter === 't_max_2m:C');
        const tempMinParam = response.data.data.find(param => param.parameter === 't_min_2m:C');
        
        if (!tempMaxParam || !tempMinParam) {
          throw new Error('Parámetros de temperatura no encontrados en la respuesta');
        }
        
        const datesMax = tempMaxParam.coordinates[0].dates;
        const datesMin = tempMinParam.coordinates[0].dates;
        
        // Asegurar que ambos arrays tengan la misma longitud
        if (datesMax.length !== datesMin.length) {
          throw new Error('Las temperaturas máximas y mínimas no coinciden en cantidad de días');
        }
        
        // Construir el array de pronóstico semanal
        const weeklyData = datesMax.map((dayMax, index) => {
          const dayMin = datesMin[index];
          return {
            date: dayMax.date,
            temp_max: dayMax.value,
            temp_min: dayMin.value
          };
        });
        
        // Asignar los datos transformados a weeklyWeather
        this.weeklyWeather = weeklyData;
        
      } catch (error) {
        console.error('Error obteniendo pronóstico semanal', error);
        this.error = error.response?.data?.detail || error.message || 'Ocurrió un error al obtener el pronóstico semanal.';
      }
    },
    
    /**
     * Determina el conditionId basado en los datos recibidos de tu API.
     * Este método puede no ser necesario para el pronóstico semanal si solo se muestran temperaturas.
     * Puedes eliminarlo si no lo utilizas.
     * @param {Object} data - Datos recibidos de la API.
     * @returns {Number} conditionId para mapear al icono.
     */
    determineConditionId(data) {
      const { t_2m, precip_1h, wind_speed_10m } = data;
      
      // Ejemplo de lógica simple:
      if (precip_1h > 10) {
        return 502; // Lluvia intensa
      } else if (wind_speed_10m > 20) {
        return 200; // Tormenta
      } else if (precip_1h > 0) {
        return 500; // Lluvia ligera
      } else if (t_2m < 0) {
        return 600; // Nieve
      } else if (t_2m >= 0 && t_2m < 10) {
        return 802; // Nublado
      } else {
        return 800; // Soleado
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

.temperature {
  margin: 0.3rem 0;
  color: #333;
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
