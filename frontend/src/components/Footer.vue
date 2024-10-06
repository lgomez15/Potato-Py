<!-- src/components/Footer.vue -->
<template>
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-links">
          <a href="#">Contacto</a>
          <a href="#">Términos y Condiciones</a>
          <a href="#">Política de Privacidad</a>
        </div>
        <div class="footer-logo">
          <p>©️ 2024 AgroMonitor</p>
        </div>
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: 'Footer',
  };
  </script>
  
  <style scoped>
  .footer {
    background-color: #4CAF50; /* Verde similar al de tu barra superior */
    color: white;
    padding: 20px 0;
    text-align: center;
    font-family: Arial, sans-serif;
    width: 100%;
  }
  
  .footer-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .footer-links {
    margin-bottom: 10px;
  }
  
  .footer-links a {
    color: white;
    margin: 0 15px;
    text-decoration: none;
  }
  
  .footer-links a:hover {
    text-decoration: underline;
  }
  
  .footer-logo p {
    margin: 0;
  }
  </style>
  