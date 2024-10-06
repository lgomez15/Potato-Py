<!-- Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h1>Agro<span>Monitor</span></h1>
    </div>
    <input type="checkbox" id="nav-toggle" class="nav-toggle" />
    <label for="nav-toggle" class="nav-toggle-label">
      <span></span>
    </label>
    <ul class="navbar-links">
      <li><router-link to="/">Inicio</router-link></li>
      <li><router-link to="/performance">Modelo de Rendimiento</router-link></li>
      <!-- Agrega más enlaces si es necesario -->
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
};
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--primary-color);
  padding: 15px 20px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-brand h1 {
  color: #fff;
  font-size: 2rem;
  margin: 0;
  font-weight: 700;
  font-family: 'Montserrat', sans-serif;
}

.navbar-brand h1 span {
  font-weight: 300;
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 20px;
}

.navbar-links li {
  font-size: 1rem;
}

.navbar-links a {
  color: #fff;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.navbar-links a:hover {
  background-color: var(--secondary-color);
}

/* Estilos para el menú responsivo */
.nav-toggle {
  display: none;
}

.nav-toggle-label {
  display: none;
}

.nav-toggle-label span {
  display: block;
  width: 28px;
  height: 3px;
  background: #fff;
  border-radius: 3px;
  position: relative;
}

.nav-toggle-label span::before,
.nav-toggle-label span::after {
  content: '';
  position: absolute;
  width: 28px;
  height: 3px;
  background: #fff;
  border-radius: 3px;
  transition: transform 0.3s ease;
}

.nav-toggle-label span::before {
  transform: translateY(-8px);
}

.nav-toggle-label span::after {
  transform: translateY(8px);
}

.nav-toggle:checked + .nav-toggle-label span {
  background: transparent;
}

.nav-toggle:checked + .nav-toggle-label span::before {
  transform: rotate(45deg);
}

.nav-toggle:checked + .nav-toggle-label span::after {
  transform: rotate(-45deg);
}

@media (max-width: 768px) {
  .navbar {
    flex-wrap: wrap;
    justify-content: space-between;
  }

  .navbar-links {
    flex-direction: column;
    width: 100%;
    display: none;
    background-color: var(--primary-color);
    padding: 10px 0;
    margin: 0;
  }

  .navbar-links li {
    text-align: center;
    margin: 10px 0;
  }

  .nav-toggle {
    display: block;
  }

  .nav-toggle-label {
    display: block;
    cursor: pointer;
  }

  .nav-toggle:checked ~ .navbar-links {
    display: flex;
  }
}
</style>
