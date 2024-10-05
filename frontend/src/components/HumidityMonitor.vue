<template>
  <div class="humidity-card" :class="humidityClass">
    <h2>Humedad del Suelo</h2>
    <p v-if="loading">Cargando...</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else>Humedad actual: {{ humidity }}%</p>
  </div>
</template>

<script>
export default {
  name: "HumidityMonitor",
  data() {
    return {
      humidity: null,
      loading: true,
      error: null,
    };
  },
  computed: {
    humidityClass() {
      if (this.humidity === null) return "";
      if (this.humidity < 30) {
        return "low"; // Rojo
      } else if (this.humidity < 60) {
        return "medium"; // Amarillo
      } else {
        return "high"; // Verde
      }
    },
  },
  methods: {
    async fetchHumidity() {
      try {
        const response = await fetch("http://localhost:8000/humidity");
        if (!response.ok) {
          throw new Error("Error al obtener datos de humedad");
        }
        const data = await response.json();
        this.humidity = data.humidity;
      } catch (error) {
        console.error("Error al obtener la humedad:", error);
        this.error = "No se pudo cargar la humedad.";
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchHumidity();
    setInterval(this.fetchHumidity, 1000);
  },
};
</script>

<style scoped>
.humidity-card {
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px;
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
  font-size: 24px;
  margin-bottom: 10px;
}

p {
  font-size: 18px;
}
</style>
