<template>
    <div>
      <h2>Gráfica de Viento</h2>
      <LineChart :chart-data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue';
  import { Line } from 'vue-chartjs';
  import { Chart, registerables } from 'chart.js';
  
  // Registrar los componentes de Chart.js
  Chart.register(...registerables);
  
  export default {
    components: {
      LineChart: Line,
    },
    props: {
      weatherData: {
        type: Object,
        required: true,
      },
    },
    setup(props) {
      const chartData = ref({
        labels: ['Velocidad del Viento', 'Dirección del Viento', 'Ráfagas de Viento'],
        datasets: [
          {
            label: 'Datos del Viento',
            backgroundColor: '#f87979',
            data: [props.weatherData.windSpeed, props.weatherData.windDirection, props.weatherData.windGusts],
          },
        ],
      });
  
      const chartOptions = ref({
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      });
  
      // Actualizar los datos del gráfico cuando cambie la información del clima
      watch(
        () => props.weatherData,
        (newData) => {
          chartData.value.datasets[0].data = [newData.windSpeed, newData.windDirection, newData.windGusts];
        },
        { deep: true }
      );
  
      return {
        chartData,
        chartOptions,
      };
    },
  };
  </script>
  
  <style scoped>
  div {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>
  