<script setup>
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Chat from './components/Chat.vue';

// Controlamos la visibilidad del chat
const isChatOpen = ref(false);

// Función para abrir/cerrar el chat
const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
};
</script>

<template>
  <div>
    <Navbar />
    <RouterView />
    
    <!-- Botón para abrir el chat -->
    <button class="chat-toggle-button" @click="toggleChat">
      <i class="fas fa-comments"></i>
    </button>

    <!-- Chat emergente -->
    <div v-if="isChatOpen" class="chat-popup">
      <Chat />
      <!-- Botón para cerrar el chat dentro de la ventana emergente -->
      <button class="close-button" @click="toggleChat"><i class="fas fa-times"></i></button>
    </div>
  </div>
</template>

<style scoped>
/* Estilo para el botón que abre el chat */
.chat-toggle-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: var(--primary-color);
  border: none;
  border-radius: 50%;
  color: white;
  width: 60px;
  height: 60px;
  font-size: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.chat-toggle-button:hover {
  background-color: var(--secondary-color);
  transform: translateY(-3px);
}

.chat-toggle-button i {
  font-size: 28px;
}

/* Estilo para la ventana emergente del chat */
.chat-popup {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 350px;
  max-width: 90%;
  height: 500px;
  max-height: 80%;
  background-color: #fff;
  border: 1px solid #ddd;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border-radius: 15px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@media (max-width: 768px) {
  .chat-popup {
    width: 100%;
    height: 100%;
    bottom: 0;
    right: 0;
    border-radius: 0;
  }
}

/* Estilo para el botón de cerrar la ventana emergente */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  color: #555;
  font-size: 20px;
  width: 30px;
  height: 30px;
  cursor: pointer;
}

.close-button:hover {
  color: var(--primary-color);
}

.close-button i {
  font-size: 24px;
}
</style>
