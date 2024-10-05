<template>
    <div class="weather-forecast">
      <h1>Previsión del Tiempo en {{ city }}</h1>
      
      <!-- Previsión de 5 días -->
      <div v-if="forecast && forecastDaily.length" class="forecast-section">
        <h2>5-Day Forecast</h2>
        <div class="forecast-container">
          <div v-for="day in forecastDaily" :key="day.date" class="forecast-day">
            <p class="date"><strong>{{ formatDate(day.date) }}</strong></p>
            <i :class="getForecastIconClass(day.conditionId)" class="weather-icon"></i>
            <p class="temperature">Min: {{ day.temp_min }} °C</p>
            <p class="temperature">Max: {{ day.temp_max }} °C</p>
            <p class="description">{{ capitalizeFirstLetter(day.description) }}</p>
          </div>
        </div>
      </div>
      
      <!-- Manejo de Errores -->
      <div v-else-if="error" class="error-message">
        <p>Error: {{ error }}</p>
      </div>
      
      <!-- Estado de Carga -->
      <div v-else class="loading-message">
        <p>Cargando datos de previsión...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import 'weather-icons/css/weather-icons.css'; // Asegúrate de importar los estilos de Weather Icons
  
  export default {
    props: {
      city: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        forecast: null,       // Datos brutos de la previsión
        forecastDaily: [],    // Previsión procesada diaria
        error: null           // Error
      };
    },
    mounted() {
      this.getForecastData(this.city);
    },
    methods: {
      /**
       * Mapea el código de condición de OpenWeatherMap al nombre de la clase de Weather Icons.
       * @param {Number} conditionId - ID de la condición del clima.
       * @returns {String} Nombre de la clase de Weather Icons.
       */
      mapConditionToIcon(conditionId) {
        if (conditionId >= 200 && conditionId < 300) {
          return 'wi-thunderstorm';
        } else if (conditionId >= 300 && conditionId < 500) {
          return 'wi-sprinkle';
        } else if (conditionId >= 500 && conditionId < 600) {
          return 'wi-rain';
        } else if (conditionId >= 600 && conditionId < 700) {
          return 'wi-snow';
        } else if (conditionId >= 700 && conditionId < 800) {
          return 'wi-fog';
        } else if (conditionId === 800) {
          return 'wi-day-sunny';
        } else if (conditionId > 800 && conditionId < 900) {
          return 'wi-cloudy';
        } else {
          return 'wi-na'; // No disponible
        }
      },
      
      /**
       * Genera la clase completa para el icono de la previsión.
       * @param {Number} conditionId - ID de la condición del clima.
       * @returns {String} Clase CSS completa para el icono.
       */
      getForecastIconClass(conditionId) {
        return `wi ${this.mapConditionToIcon(conditionId)}`;
      },
      
      /**
       * Genera la URL completa para el icono del clima.
       * @param {String} iconCode - Código del icono proporcionado por la API.
       * @returns {String} URL del icono.
       */
      getIconUrl(iconCode) {
        return `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
      },
      
      /**
       * Capitaliza la primera letra de una cadena de texto.
       * @param {String} text - Texto a capitalizar.
       * @returns {String} Texto capitalizado.
       */
      capitalizeFirstLetter(text) {
        if (!text) return '';
        return text.charAt(0).toUpperCase() + text.slice(1);
      },
      
      /**
       * Obtiene los datos de la previsión desde la API de OpenWeatherMap.
       * @param {String} city - Nombre de la ciudad.
       */
      async getForecastData(city) {
        const apiKey = 'd2736c1d75667857ddcc39a3dc4651c3'; // Reemplaza con tu clave de API
        const forecastUrl = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&units=metric&appid=${apiKey}`;
        
        try {
          const response = await axios.get(forecastUrl);
          this.forecast = response.data;
          console.log(this.forecast); // Verifica los datos de la previsión en la consola
          this.processForecastData();
        } catch (error) {
          console.error('Error fetching forecast data', error);
          this.error = 'No se pudieron obtener los datos de previsión. Por favor, verifica la clave de API o el endpoint.';
        }
      },
      
      /**
       * Procesa los datos brutos de la previsión para obtener información diaria.
       */
      processForecastData() {
        if (!this.forecast || !this.forecast.list) return;
        
        const dailyData = {};
        
        this.forecast.list.forEach(entry => {
          const date = entry.dt_txt.split(' ')[0];
          
          if (!dailyData[date]) {
            dailyData[date] = {
              temp_min: entry.main.temp_min,
              temp_max: entry.main.temp_max,
              description: entry.weather[0].description,
              conditionId: entry.weather[0].id, // Almacenar el ID de la condición
              count: 1
            };
          } else {
            dailyData[date].temp_min = Math.min(dailyData[date].temp_min, entry.main.temp_min);
            dailyData[date].temp_max = Math.max(dailyData[date].temp_max, entry.main.temp_max);
            dailyData[date].count += 1;
            // Opcional: Mejorar la descripción agregando lógica para seleccionar la descripción más frecuente
            // Opcional: Podrías decidir qué icono usar basado en la hora del día o la prevalencia
          }
        });
        
        // Convertir el objeto en un array y excluir el día actual si ya está mostrado en el clima actual
        const today = new Date().toISOString().split('T')[0];
        this.forecastDaily = Object.keys(dailyData)
          .filter(date => date !== today)
          .map(date => ({
            date,
            temp_min: dailyData[date].temp_min.toFixed(1),
            temp_max: dailyData[date].temp_max.toFixed(1),
            description: dailyData[date].description,
            conditionId: dailyData[date].conditionId // Incluir el ID de la condición
          }));
      },
      
      /**
       * Formatea una cadena de fecha a un formato legible.
       * @param {String} dateString - Cadena de fecha en formato ISO.
       * @returns {String} Fecha formateada.
       */
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
      }
    }
  };
  </script>
  
  <style scoped>
  .weather-forecast {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 2rem;
    background: linear-gradient(135deg, #ece9e6, #ffffff);
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
  }
  
  .forecast-section {
    text-align: center;
  }
  
  .forecast-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
  }
  
  .forecast-day {
    background: linear-gradient(135deg, #f6f9fc, #e9eff5);
    padding: 1.5rem;
    border-radius: 12px;
    width: 160px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .forecast-day:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  .date {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 0.5rem;
  }
  
  .weather-icon {
    font-size: 36px;
    color: #ff9800;
    margin-bottom: 0.5rem;
  }
  
  .temperature {
    font-size: 0.95rem;
    color: #333;
    margin: 0.25rem 0;
  }
  
  .description {
    font-size: 0.9rem;
    color: #666;
  }
  
  .error-message, .loading-message {
    text-align: center;
    margin-top: 2rem;
    color: #d32f2f;
    font-weight: bold;
  }
  
  @media (max-width: 600px) {
    .forecast-container {
      flex-direction: column;
      align-items: center;
    }
    
    .forecast-day {
      width: 80%;
    }
  }
  </style>
  