<template>
    <div class="information-panel">
      <!-- Panel de Información de Clima -->
      <h1 class="title">Weather Information</h1>
      
      <div class="info-cards">
        <!-- Card de Humedad -->
        <div class="info-card">
          <h2>Humedad</h2>
          <p>{{ weatherData.humidity }}%</p>
        </div>
        
        <!-- Card de Temperatura --> 
        <div class="info-card">
          <h2>Temperatura</h2>
          <p>{{ weatherData.temperature }}°C</p>
        </div>
        
        <!-- Card de Alertas -->
        <div class="info-card big-card">
          <h2>Alertas</h2>
          <p>{{ weatherData.alerts }}</p>
        </div>
        
        <!-- Card de Recomendaciones -->
        <div class="info-card">
          <h2>Recomendación</h2>
          <p>{{ weatherData.recommendation }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InformationPanel',
    data() {
      return {
        weatherData: {
          humidity: 65,
          temperature: 22,
          alerts: 'Lluvias ligeras en la tarde',
          recommendation: 'Llevar paraguas y abrigarse bien'
        }
      };
    }
  };
  </script>
  
  <style scoped>
  /* Estilo del contenedor general */
  .information-panel {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background-color: #f4f4f9;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 1000px;
    margin: 20px auto;
  }
  
  /* Estilo del título */
  .title {
    font-size: 2em;
    margin-bottom: 20px;
    color: #333;
    text-align: center;
  }
  
  /* Contenedor de las tarjetas */
  .info-cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }
  
  /* Estilo de cada tarjeta */
  .info-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    text-align: center;
    width: 200px;
    transition: transform 0.3s ease;
  }
  
  .info-card:hover {
    transform: translateY(-5px);
  }
  
  /* Estilo del texto en las tarjetas */
  .info-card h2 {
    font-size: 1.5em;
    margin-bottom: 10px;
    color: #555;
  }
  
  .info-card p {
    font-size: 1.2em;
    margin: 0;
    color: #111;
  }
  
  /* Tarjeta más grande para las alertas */
  .big-card {
    width: 420px;
  }
  
  /* Efecto de animación en hover */
  .info-card:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  }
  
  @media (max-width: 768px) {
    /* Ajuste de tarjetas en pantallas pequeñas */
    .info-card {
      width: 100%;
    }
  
    .big-card {
      width: 100%;
    }
  }
  </style>
  