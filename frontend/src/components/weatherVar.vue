<template>
  <div class="weather-forecast">
    <h1>Tiempo Actual en {{ city }}</h1>
    
    <!-- Mostrar el tiempo actual -->
    <div v-if="currentWeather" class="current-weather-section">
      <h2>Hoy</h2>
      <div class="current-weather-container">
        <i :class="getWeatherIconClass(currentWeather.conditionId)" class="weather-icon"></i>
        <p class="temperature">Temperatura: {{ currentWeather.temperature }} °C</p>
        <p class="wind">Viento: {{ currentWeather.wind_speed }} km/h, Dirección: {{ currentWeather.wind_dir }}°</p>
        <p class="gusts">Ráfagas: {{ currentWeather.wind_gusts }} km/h</p>
        <p class="precipitation">Precipitación (1h): {{ currentWeather.precip_1h }} mm</p>
        <p class="precipitation">Precipitación (24h): {{ currentWeather.precip_24h }} mm</p>
      </div>
    </div>
    
    <!-- Manejo de Errores -->
    <div v-else-if="error" class="error-message">
      <p>Error: {{ error }}</p>
    </div>
    
    <!-- Estado de Carga -->
    <div v-else class="loading-message">
      <p>Cargando datos de tiempo actual...</p>
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
      currentWeather: null, // Datos del tiempo actual
      error: null           // Error
    };
  },
  mounted() {
    this.fetchCurrentWeather(this.city);
  },
  methods: {
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
     * Mapea el código de condición de Meteomatics al nombre de la clase de Weather Icons.
     * @param {Number} conditionId - ID de la condición del clima.
     * @returns {String} Nombre de la clase de Weather Icons.
     */
    mapConditionToIcon(conditionId) {
      // Deberás ajustar este mapeo según los códigos de condición que devuelve tu API
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
     * Genera la clase completa para el icono del clima.
     * @param {Number} conditionId - ID de la condición del clima.
     * @returns {String} Clase CSS completa para el icono.
     */
    getWeatherIconClass(conditionId) {
      return `wi ${this.mapConditionToIcon(conditionId)}`;
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
     * Obtiene los datos del tiempo actual desde tu API.
     * @param {String} city - Nombre de la ciudad.
     */
async fetchCurrentWeather(city) {
try {
  // Obtener las coordenadas de la ciudad usando el endpoint de geocodificación
  const { latitude, longitude } = await this.getCoordinates(city);
  
  // Obtener la fecha y hora actual en formato ISO
  const currentDatetime = new Date().toISOString();
  
  // Construir la URL de tu API
  const apiUrl = `http://127.0.0.1:8000/weather/${encodeURIComponent(currentDatetime)}/${latitude},${longitude}`;
  
  // Realizar la petición a tu API
  const response = await axios.get(apiUrl);
  
  // Verificar si la respuesta tiene la estructura esperada
  if (!response.data || !Array.isArray(response.data.data)) {
    throw new Error('Estructura de respuesta inesperada');
  }
  
  // Crear un objeto para almacenar los datos transformados
  const weatherData = {};
  
  // Recorrer cada parámetro en la respuesta
  response.data.data.forEach(paramObj => {
    const parameter = paramObj.parameter; // Ejemplo: "t_2m:C"
    
    // Extraer el nombre del parámetro sin el sufijo
    const key = parameter.split(':')[0]; // "t_2m"
    
    // Obtener el valor
    const value = paramObj.coordinates[0].dates[0].value; // Por ejemplo, 25.4
    
    // Asignar el valor al objeto weatherData
    weatherData[key] = value;
  });
  
  // Asignar los datos transformados a currentWeather
  this.currentWeather = {
    temperature: weatherData.t_2m,
    wind_speed: weatherData.wind_speed_10m,
    wind_dir: weatherData.wind_dir_10m,
    wind_gusts: weatherData.wind_gusts_10m_1h,
    precip_1h: weatherData.precip_1h,
    precip_24h: weatherData.precip_24h,
    conditionId: this.determineConditionId(weatherData) // Función para determinar conditionId
  };
  
  // Imprimir la temperatura en la consola
  console.log("temperatura", this.currentWeather.temperature);
  
} catch (error) {
  console.error('Error obteniendo datos del tiempo actual', error);
  this.error = error.response?.data?.detail || error.message || 'Ocurrió un error al obtener los datos del tiempo actual.';
}
},

    
    /**
     * Determina el conditionId basado en los datos recibidos de tu API.
     * @param {Object} data - Datos recibidos de la API.
     * @returns {Number} conditionId para mapear al icono.
     */
determineConditionId(data) {
      const { t_2m, precip_1h, wind_speed_10m} = data;
      
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
.weather-forecast {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem;
  background: linear-gradient(135deg, #ece9e6, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.current-weather-section {
  text-align: center;
}

.current-weather-container {
  background: linear-gradient(135deg, #f6f9fc, #e9eff5);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: inline-block;
}

.weather-icon {
  font-size: 48px;
  color: #ff9800;
  margin-bottom: 1rem;
}

.temperature, .wind, .gusts, .precipitation {
  font-size: 1rem;
  color: #333;
  margin: 0.5rem 0;
}

.error-message, .loading-message {
  text-align: center;
  margin-top: 2rem;
  color: #d32f2f;
  font-weight: bold;
}

@media (max-width: 600px) {
  .current-weather-container {
    width: 100%;
    padding: 1rem;
  }
  
  .weather-icon {
    font-size: 36px;
  }
}
</style><template>
  <div class="weather-forecast">
    <h1>Tiempo Actual en {{ city }}</h1>
    
    <!-- Mostrar el tiempo actual -->
    <div v-if="currentWeather" class="current-weather-section">
      <h2>Hoy</h2>
      <div class="current-weather-container">
        <i :class="getWeatherIconClass(currentWeather.conditionId)" class="weather-icon"></i>
        <p class="temperature">Temperatura: {{ currentWeather.temperature }} °C</p>
        <p class="wind">Viento: {{ currentWeather.wind_speed }} km/h, Dirección: {{ currentWeather.wind_dir }}°</p>
        <p class="gusts">Ráfagas: {{ currentWeather.wind_gusts }} km/h</p>
        <p class="precipitation">Precipitación (1h): {{ currentWeather.precip_1h }} mm</p>
        <p class="precipitation">Precipitación (24h): {{ currentWeather.precip_24h }} mm</p>
      </div>
    </div>
    
    <!-- Manejo de Errores -->
    <div v-else-if="error" class="error-message">
      <p>Error: {{ error }}</p>
    </div>
    
    <!-- Estado de Carga -->
    <div v-else class="loading-message">
      <p>Cargando datos de tiempo actual...</p>
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
      currentWeather: null, // Datos del tiempo actual
      error: null           // Error
    };
  },
  mounted() {
    this.fetchCurrentWeather(this.city);
  },
  methods: {
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
     * Mapea el código de condición de Meteomatics al nombre de la clase de Weather Icons.
     * @param {Number} conditionId - ID de la condición del clima.
     * @returns {String} Nombre de la clase de Weather Icons.
     */
    mapConditionToIcon(conditionId) {
      // Deberás ajustar este mapeo según los códigos de condición que devuelve tu API
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
     * Genera la clase completa para el icono del clima.
     * @param {Number} conditionId - ID de la condición del clima.
     * @returns {String} Clase CSS completa para el icono.
     */
    getWeatherIconClass(conditionId) {
      return `wi ${this.mapConditionToIcon(conditionId)}`;
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
     * Obtiene los datos del tiempo actual desde tu API.
     * @param {String} city - Nombre de la ciudad.
     */
async fetchCurrentWeather(city) {
try {
  // Obtener las coordenadas de la ciudad usando el endpoint de geocodificación
  const { latitude, longitude } = await this.getCoordinates(city);
  
  // Obtener la fecha y hora actual en formato ISO
  const currentDatetime = new Date().toISOString();
  
  // Construir la URL de tu API
  const apiUrl = `http://127.0.0.1:8000/weather/${encodeURIComponent(currentDatetime)}/${latitude},${longitude}`;
  
  // Realizar la petición a tu API
  const response = await axios.get(apiUrl);
  
  // Verificar si la respuesta tiene la estructura esperada
  if (!response.data || !Array.isArray(response.data.data)) {
    throw new Error('Estructura de respuesta inesperada');
  }
  
  // Crear un objeto para almacenar los datos transformados
  const weatherData = {};
  
  // Recorrer cada parámetro en la respuesta
  response.data.data.forEach(paramObj => {
    const parameter = paramObj.parameter; // Ejemplo: "t_2m:C"
    
    // Extraer el nombre del parámetro sin el sufijo
    const key = parameter.split(':')[0]; // "t_2m"
    
    // Obtener el valor
    const value = paramObj.coordinates[0].dates[0].value; // Por ejemplo, 25.4
    
    // Asignar el valor al objeto weatherData
    weatherData[key] = value;
  });
  
  // Asignar los datos transformados a currentWeather
  this.currentWeather = {
    temperature: weatherData.t_2m,
    wind_speed: weatherData.wind_speed_10m,
    wind_dir: weatherData.wind_dir_10m,
    wind_gusts: weatherData.wind_gusts_10m_1h,
    precip_1h: weatherData.precip_1h,
    precip_24h: weatherData.precip_24h,
    conditionId: this.determineConditionId(weatherData) // Función para determinar conditionId
  };
  
  // Imprimir la temperatura en la consola
  console.log("temperatura", this.currentWeather.temperature);
  
} catch (error) {
  console.error('Error obteniendo datos del tiempo actual', error);
  this.error = error.response?.data?.detail || error.message || 'Ocurrió un error al obtener los datos del tiempo actual.';
}
},

    
    /**
     * Determina el conditionId basado en los datos recibidos de tu API.
     * @param {Object} data - Datos recibidos de la API.
     * @returns {Number} conditionId para mapear al icono.
     */
determineConditionId(data) {
      const { t_2m, precip_1h, wind_speed_10m} = data;
      
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
.weather-forecast {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem;
  background: linear-gradient(135deg, #ece9e6, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.current-weather-section {
  text-align: center;
}

.current-weather-container {
  background: linear-gradient(135deg, #f6f9fc, #e9eff5);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: inline-block;
}

.weather-icon {
  font-size: 48px;
  color: #ff9800;
  margin-bottom: 1rem;
}

.temperature, .wind, .gusts, .precipitation {
  font-size: 1rem;
  color: #333;
  margin: 0.5rem 0;
}

.error-message, .loading-message {
  text-align: center;
  margin-top: 2rem;
  color: #d32f2f;
  font-weight: bold;
}

@media (max-width: 600px) {
  .current-weather-container {
    width: 100%;
    padding: 1rem;
  }
  
  .weather-icon {
    font-size: 36px;
  }
}
</style>