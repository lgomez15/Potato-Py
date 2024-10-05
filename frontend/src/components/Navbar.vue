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
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #4CAF50; /* Cambia el color según tu preferencia */
  padding: 10px 20px;
}

.navbar-logo {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px; /* Ajusta el tamaño del logo */
  margin-right: 10px;
}

.navbar-links {
  list-style-type: none;
  display: flex;
  gap: 20px;
}

.navbar-links li {
  font-size: 16px; /* Ajusta el tamaño de la fuente según tu preferencia */
}

.navbar-links a {
  color: white; /* Cambia el color del texto */
  text-decoration: none;
}

.navbar-links a:hover {
  text-decoration: underline; /* Efecto hover */
}
</style>
