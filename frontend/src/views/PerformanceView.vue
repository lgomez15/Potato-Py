<template>
  <div class="prediction-container">
    <h2>Predicción de Crecimiento del Tallo</h2>
    <form @submit.prevent="predecirCrecimiento" class="prediction-form">
      <!-- Campos de entrada con sliders -->
      <div class="slider-group" v-for="(param, index) in parametros" :key="index">
        <label :for="param.name">{{ param.label }}: <span>{{ param.value }}</span></label>
        <input
          type="range"
          :id="param.name"
          v-model="param.value"
          :min="param.min"
          :max="param.max"
          :step="param.step"
        />
      </div>

      <button type="submit" class="submit-button">Predecir</button>
    </form>

    <div v-if="resultado" class="result-container">
      <h3>Predicción: {{ resultado.predicted_stem_growth }}</h3>
      <h4>Categoría: {{ resultado.categoria }}</h4>

      <!-- Contenedor de la animación -->
      <div class="animation-container">
        <svg
          ref="plantSvg"
          id="plant-svg"
          viewBox="0 0 200 200"
          xmlns="http://www.w3.org/2000/svg"
        >
          <!-- Tallo -->
          <rect
            id="stem"
            x="95"
            y="100"
            width="10"
            height="0"
            fill="#8B5A2B"
          />
          <!-- Hoja izquierda -->
          <path
            id="left-leaf"
            d="M95 150 Q70 130 95 110"
            fill="green"
            opacity="0"
          />
          <!-- Hoja derecha -->
          <path
            id="right-leaf"
            d="M105 150 Q130 130 105 110"
            fill="green"
            opacity="0"
          />
          <!-- Fruto -->
          <circle
            id="fruit"
            cx="100"
            cy="90"
            r="0"
            fill="red"
            opacity="0"
          />
        </svg>
      </div>

      <!-- Barra de progreso debajo de la animación -->
      <div class="progress-bar">
        <div class="progress-fill" :style="progressFillStyle"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { gsap } from 'gsap';

export default {
  data() {
    return {
      parametros: [
        { name: 'week_of_year', label: 'Semana del Año', value: 1, min: 1, max: 52, step: 1 },
        { name: 'row', label: 'Fila', value: 1, min: 1, max: 100, step: 1 },
        { name: 'column', label: 'Columna', value: 1, min: 1, max: 100, step: 1 },
        { name: 'plant_id', label: 'ID de Planta', value: 1, min: 1, max: 1000, step: 1 },
        { name: 'stem_diameter', label: 'Diámetro del Tallo', value: 0.5, min: 0.1, max: 10, step: 0.1 },
        { name: 'highest_truss', label: 'Racimo Más Alto', value: 1, min: 1, max: 20, step: 1 },
        { name: 'temp_mean', label: 'Temperatura Media (°C)', value: 20, min: -10, max: 50, step: 0.1 },
        { name: 'temp_min', label: 'Temperatura Mínima (°C)', value: 15, min: -20, max: 40, step: 0.1 },
        { name: 'temp_max', label: 'Temperatura Máxima (°C)', value: 25, min: -5, max: 60, step: 0.1 },
        { name: 'humidity_mean', label: 'Humedad Media (%)', value: 50, min: 0, max: 100, step: 1 },
        { name: 'humidity_min', label: 'Humedad Mínima (%)', value: 30, min: 0, max: 100, step: 1 },
        { name: 'humidity_max', label: 'Humedad Máxima (%)', value: 70, min: 0, max: 100, step: 1 },
      ],
      resultado: null,
    };
  },
  computed: {
    progressFillStyle() {
      if (!this.resultado) return { width: '0%' };
      let width = '0%';
      let backgroundColor = '#4caf50'; // Color por defecto (verde)

      switch (this.resultado.categoria.toLowerCase()) {
        case 'alto':
          width = '100%';
          backgroundColor = 'green';
          break;
        case 'medio':
          width = '66%';
          backgroundColor = 'yellow';
          break;
        case 'bajo':
          width = '33%';
          backgroundColor = 'red';
          break;
        default:
          width = '0%';
      }

      return {
        width,
        backgroundColor,
        transition: 'width 1s ease-in-out',
      };
    },
  },
  watch: {
    resultado(newVal) {
      if (newVal) {
        this.animatePlant(newVal.categoria.toLowerCase());
      }
    },
  },
  methods: {
    async predecirCrecimiento() {
      const datos = {};
      this.parametros.forEach(param => {
        datos[param.name] = param.value;
      });

      const respuesta = await fetch("http://35.187.77.55:8000/predict/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datos),
      });
      this.resultado = await respuesta.json();
    },
    animatePlant(category) {
      // Reinicia las animaciones anteriores
      gsap.killTweensOf("*");
      gsap.set("#stem", { height: 0, y: 100 });
      gsap.set("#left-leaf", { opacity: 0 });
      gsap.set("#right-leaf", { opacity: 0 });
      gsap.set("#fruit", { r: 0, opacity: 0 });

      if (category === 'alto') {
        // Animación para alto rendimiento
        gsap.to("#stem", { height: 100, y: 0, duration: 1 });
        gsap.to("#left-leaf", { opacity: 1, duration: 1, delay: 1 });
        gsap.to("#right-leaf", { opacity: 1, duration: 1, delay: 1 });
        gsap.to("#fruit", { r: 10, opacity: 1, duration: 1, delay: 2 });
      } else if (category === 'medio') {
        // Animación para rendimiento medio
        gsap.to("#stem", { height: 70, y: 30, duration: 1 });
        gsap.to("#left-leaf", { opacity: 1, duration: 1, delay: 1 });
        gsap.to("#right-leaf", { opacity: 0, duration: 0 });
        gsap.to("#fruit", { r: 5, opacity: 1, duration: 1, delay: 2 });
      } else if (category === 'bajo') {
        // Animación para bajo rendimiento
        gsap.to("#stem", { height: 40, y: 60, duration: 1 });
        gsap.to("#left-leaf", { opacity: 0, duration: 0 });
        gsap.to("#right-leaf", { opacity: 0, duration: 0 });
        gsap.to("#fruit", { r: 0, opacity: 0, duration: 0 });
      }
    },
  },
};
</script>

<style scoped>
/* Contenedor principal */
.prediction-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 40px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2.5rem;
  color: var(--primary-color);
  font-weight: 700;
  font-family: 'Montserrat', sans-serif;
}

.prediction-form {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.slider-group {
  flex: 1 1 calc(50% - 30px);
  display: flex;
  flex-direction: column;
}

.slider-group label {
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--text-color);
  font-size: 1rem;
}

.slider-group label span {
  color: var(--secondary-color);
  font-weight: normal;
}

.slider-group input[type="range"] {
  -webkit-appearance: none;
  width: 100%;
  height: 10px;
  border-radius: 5px;
  background: #e0e0e0;
  outline: none;
}

.slider-group input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
}

.slider-group input[type="range"]::-webkit-slider-thumb:hover {
  background: var(--accent-color);
}

.slider-group input[type="range"]::-moz-range-thumb {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
}

.slider-group input[type="range"]::-moz-range-thumb:hover {
  background: var(--accent-color);
}

.submit-button {
  padding: 15px 30px;
  background-color: var(--primary-color);
  color: #fff;
  font-size: 1.2em;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  align-self: center;
  margin-top: 20px;
}

.submit-button:hover {
  background-color: var(--secondary-color);
}

.result-container {
  margin-top: 40px;
  background-color: #f9f9f9;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
}

.result-container h3,
.result-container h4 {
  margin: 10px 0;
  color: var(--text-color);
}

.result-container h3 {
  font-size: 2rem;
  font-weight: bold;
}

.result-container h4 {
  font-size: 1.5rem;
  color: var(--secondary-color);
}

/* Estilos para la animación */
.animation-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

#plant-svg {
  width: 200px;
  height: 200px;
}

/* Estilos para la barra de progreso */
.progress-bar {
  position: relative;
  width: 100%;
  height: 30px;
  background-color: #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
  margin-top: 20px;
}

.progress-fill {
  height: 100%;
  width: 0;
  background-color: var(--primary-color);
}

/* Responsividad */
@media (max-width: 768px) {
  .prediction-container {
    padding: 20px;
    margin: 20px;
  }

  .slider-group {
    flex: 1 1 100%;
  }

  .submit-button {
    width: 100%;
  }
}
</style>