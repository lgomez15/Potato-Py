<template>
  <nav class="navbar">
    <div class="navbar-logo">
      <img src="../assets/logo.svg" alt="Logo" class="logo" />
      <h1>Clima en el Campo</h1>
    </div>
    <ul class="navbar-links">
      <li><router-link to="/">Dashboard</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
};
</script>

<style scoped>
/* Estilos para la barra de navegación */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50; /* Fondo oscuro y elegante */
  padding: 15px 30px; /* Espaciado interno */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra para profundidad */
  border-bottom: 3px solid #2980b9; /* Línea inferior decorativa */
  position: sticky; /* Fijar barra de navegación en la parte superior */
  top: 0;
  z-index: 1000; /* Asegura que siempre esté encima de otros elementos */
}

.navbar-logo {
  display: flex;
  align-items: center;
}

.logo {
  height: 50px; /* Tamaño del logo ajustado */
  margin-right: 15px; /* Espacio entre el logo y el título */
}

h1 {
  color: white;
  font-size: 1.8em; /* Tamaño de fuente más grande para el título */
  margin: 0;
}

/* Estilos para los enlaces de la barra de navegación */
.navbar-links {
  list-style-type: none;
  display: flex;
  gap: 30px; /* Separación entre los enlaces */
}

.navbar-links li {
  font-size: 1.1em; /* Tamaño de fuente ligeramente más grande */
}

.navbar-links a {
  color: white;
  text-decoration: none;
  padding: 8px 16px; /* Espaciado dentro del enlace */
  border-radius: 6px; /* Bordes suaves para los enlaces */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Transiciones suaves */
}

.navbar-links a:hover {
  background-color: #2980b9; /* Fondo azul más oscuro al hacer hover */
  transform: translateY(-2px); /* Ligeramente elevado al pasar el cursor */
}

/* Responsive: Ajustes para pantallas más pequeñas */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 10px 20px;
  }

  .navbar-links {
    gap: 15px; /* Reducir el espacio entre los enlaces en pantallas pequeñas */
    flex-direction: column; /* Alinear los enlaces en columna */
    width: 100%; /* Ocupa todo el ancho disponible */
  }

  h1 {
    font-size: 1.5em; /* Reducir ligeramente el tamaño del título */
  }

  .logo {
    height: 40px; /* Logo más pequeño en pantallas pequeñas */
  }
}

@media (min-width: 1200px) {
  .navbar-links {
    gap: 40px; /* Mayor separación entre enlaces en pantallas grandes */
  }

  .logo {
    height: 60px; /* Logo más grande en pantallas grandes */
  }

  h1 {
    font-size: 2.2em; /* Mayor tamaño del título en pantallas grandes */
  }
}
</style>
