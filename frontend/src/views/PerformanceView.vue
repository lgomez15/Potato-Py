<template>
  <div class="prediction-container">
    <h2>Predicción de Stem Growth</h2>
    <form @submit.prevent="predecirCrecimiento" class="prediction-form">
      <!-- Campos de entrada -->
      <div class="form-group">
        <input v-model="week_of_year" placeholder="Week of Year" type="number" />
      </div>
      <div class="form-group">
        <input v-model="row" placeholder="Row" type="number" />
      </div>
      <div class="form-group">
        <input v-model="column" placeholder="Column" type="number" />
      </div>
      <div class="form-group">
        <input v-model="plant_id" placeholder="Plant ID" type="number" />
      </div>
      <div class="form-group">
        <input v-model="stem_diameter" placeholder="Stem Diameter" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="highest_truss" placeholder="Highest Truss" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="temp_mean" placeholder="Temp Mean" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="temp_min" placeholder="Temp Min" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="temp_max" placeholder="Temp Max" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="humidity_mean" placeholder="Humidity Mean" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="humidity_min" placeholder="Humidity Min" type="number" step="0.01" />
      </div>
      <div class="form-group">
        <input v-model="humidity_max" placeholder="Humidity Max" type="number" step="0.01" />
      </div>

      <button type="submit" class="submit-button">Predecir</button>
    </form>

    <div v-if="resultado" class="result-container">
      <h3>Predicción: {{ resultado.predicted_stem_growth }}</h3>
      <h4>Categoría: {{ resultado.categoria }}</h4>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      week_of_year: '',
      row: '',
      column: '',
      plant_id: '',
      stem_diameter: '',
      highest_truss: '',
      temp_mean: '',
      temp_min: '',
      temp_max: '',
      humidity_mean: '',
      humidity_min: '',
      humidity_max: '',
      resultado: null,
    };
  },
  methods: {
    async predecirCrecimiento() {
      const datos = {
        week_of_year: this.week_of_year,
        row: this.row,
        column: this.column,
        plant_id: this.plant_id,
        stem_diameter: this.stem_diameter,
        highest_truss: this.highest_truss,
        temp_mean: this.temp_mean,
        temp_min: this.temp_min,
        temp_max: this.temp_max,
        humidity_mean: this.humidity_mean,
        humidity_min: this.humidity_min,
        humidity_max: this.humidity_max,
      };

      const respuesta = await fetch("http://localhost:5515/predict/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datos),
      });
      this.resultado = await respuesta.json();
    },
  },
};
</script>

<style scoped>
/* Contenedor principal */
.prediction-container {
  max-width: 600px;
  margin: 0 auto;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

/* Estilos para el formulario */
.prediction-form {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.form-group {
  flex: 1 1 45%; /* Ajuste automático en 2 columnas */
  min-width: 200px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

input:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

/* Estilos del botón */
.submit-button {
  padding: 12px 20px;
  background-color: #3498db;
  color: #fff;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  margin-top: 15px;
}

.submit-button:hover {
  background-color: #2980b9;
}

/* Estilos para el contenedor del resultado */
.result-container {
  margin-top: 20px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  text-align: center;
}

h3, h4 {
  margin: 10px 0;
}
</style>
