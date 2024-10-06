<template>
  <div class="sensor-matrix-container">
    <!-- Encabezado con el título y el botón "Simular Fallo" -->
    <div class="header">
      <h2>Parcela</h2>
      <button @click="toggleDataSource">{{ buttonLabel }}</button>
    </div>

    <!-- Matriz de Sensores -->
    <div class="sensor-matrix">
      <div
        v-for="sensor in sensors"
        :key="sensor.id"
        class="sensor-cell"
        :style="getSensorStyle(sensor.humedadDetectada)"
        @mouseover="showTooltip(sensor, $event)"
        @mouseleave="hideTooltip"
      >
        <!-- Puedes agregar contenido dentro de cada celda si lo deseas -->
      </div>
    </div>

    <!-- Área de Alertas -->
    <div class="alerts-container">
      <h3>Alertas Moderadas</h3>
      <ul>
        <li v-for="sensor in moderateAlerts" :key="sensor.id">
          {{ sensor.name }}: {{ parseFloat(sensor.humedadDetectada.replace('%', '')).toFixed(1) }}%
        </li>
      </ul>
      <h3>Alertas Altas</h3>
      <ul>
        <li v-for="sensor in highAlerts" :key="sensor.id">
          {{ sensor.name }}: {{ parseFloat(sensor.humedadDetectada.replace('%', '')).toFixed(1) }}%
        </li>
      </ul>
    </div>

    <!-- Tooltip -->
    <div v-if="tooltip.visible" :style="tooltip.style" class="tooltip">
      <p>{{ tooltip.text }}</p>
    </div>

    <!-- Mensaje de Error (Opcional) -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'SensorsView',
  data() {
    return {
      sensors: [],
      error: null,
      tooltip: {
        visible: false,
        text: '',
        style: {},
      },
      rows: 3, // Número de filas en la matriz
      columns: 3, // Número de columnas en la matriz
      dataSource: 'A', // 'A' para sensors, 'B' para sensorsB
    };
  },
  mounted() {
    this.fetchSensorData();
    this.interval = setInterval(this.fetchSensorData, 2000); // Actualiza cada 2 segundos
  },
  beforeUnmount() {
    clearInterval(this.interval); // Limpia el intervalo cuando el componente se desmonta
  },
  computed: {
    moderateAlerts() {
      return this.sensors.filter(sensor => {
        const humidity = parseFloat(sensor.humedadDetectada.replace('%', ''));
        return humidity >= 25 && humidity <= 75;
      });
    },
    highAlerts() {
      return this.sensors.filter(sensor => {
        const humidity = parseFloat(sensor.humedadDetectada.replace('%', ''));
        return humidity < 25;
      });
    },
    buttonLabel() {
      return this.dataSource === 'A' ? 'Simular Fallo' : 'Restablecer Datos';
    },
  },
  methods: {
    async fetchSensorData() {
      const url =
        this.dataSource === 'A'
          ? 'http://35.187.77.55:8000/sensorsG'
          : 'http://35.187.77.55:8000/sensorsB';
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Error al obtener datos de los sensores');
        const data = await response.json();
        this.sensors = data;
        this.error = null; // Reiniciar el error si la solicitud es exitosa
      } catch (err) {
        console.error('Error al obtener los datos:', err);
        this.error = 'No se pudo cargar los datos de los sensores.';
      }
    },
    toggleDataSource() {
      // Cambiar la fuente de datos
      this.dataSource = this.dataSource === 'A' ? 'B' : 'A';
      // Volver a obtener los datos con la nueva fuente
      this.fetchSensorData();
    },
    getSensorStyle(humedad) {
      const humidityValue = parseFloat(humedad.replace('%', ''));
      const color = this.getColorByHumidity(humidityValue);

      return {
        backgroundColor: color,
        transition: 'background-color 1s ease',
      };
    },
    getColorByHumidity(humidity) {
      // Mapea el valor de humedad a un color pastel
      if (humidity > 75) {
        return '#A8E6CF'; // Verde pastel
      } else if (humidity >= 25 && humidity <= 75) {
        return '#FFD3B6'; // Amarillo pastel
      } else {
        return '#FF8A80'; // Rojo pastel
      }
    },
    showTooltip(sensor, event) {
      const humidityValue = parseFloat(sensor.humedadDetectada.replace('%', '')).toFixed(1);
      this.tooltip.visible = true;
      this.tooltip.text = `${sensor.name}: ${humidityValue}%`;
      this.tooltip.style = {
        top: event.clientY + 10 + 'px',
        left: event.clientX + 10 + 'px',
      };
    },
    hideTooltip() {
      this.tooltip.visible = false;
    },
  },
};
</script>

<style scoped>
.sensor-matrix-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  text-align: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  font-size: 2rem;
  color: var(--primary-color);
  font-family: 'Montserrat', sans-serif;
}

.header button {
  padding: 10px 20px;
  background-color: #f44336; /* Color rojo para simular fallo */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.header button:hover {
  background-color: #d32f2f;
}

/* Matriz de Sensores */
.sensor-matrix {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Ajusta el número de columnas */
  grid-gap: 10px;
  margin-bottom: 30px;
}

.sensor-cell {
  width: 100%;
  padding-bottom: 100%; /* Para mantener las celdas cuadradas */
  position: relative;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}

.sensor-cell:hover {
  transform: translateY(-5px);
}

/* Tooltip */
.tooltip {
  position: fixed;
  background-color: #fff;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.tooltip p {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

/* Estilos para el área de alertas */
.alerts-container {
  text-align: left;
  margin-top: 20px;
}

.alerts-container h3 {
  font-size: 1.5rem;
  color: var(--primary-color);
  margin-bottom: 10px;
}

.alerts-container ul {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.alerts-container li {
  font-size: 1rem;
  margin-bottom: 5px;
  padding: 8px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.alerts-container li:hover {
  background-color: #e0e0e0;
}

/* Mensaje de Error */
.error-message {
  color: red;
  margin-top: 20px;
  font-weight: bold;
}

/* Responsividad */
@media (max-width: 600px) {
  .sensor-matrix {
    grid-template-columns: repeat(2, 1fr);
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header button {
    margin-top: 10px;
    width: 100%;
  }
}
</style>
