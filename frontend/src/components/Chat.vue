<template>
  <div class="chat-container">
    <div class="chat-header">
      <!-- Botón con icono de papelera para limpiar el chat -->
      <button class="clear-chat-button" @click="clearChat">🗑️</button>
      <h2>Asistente Virtual</h2>
    </div>
    <div class="chat-window" ref="chatWindow">
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        :class="['message', msg.sender]"
      >
        <p>{{ msg.text }}</p>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="input-form">
      <input
        type="text"
        v-model="userInput"
        placeholder="Escribe tu pregunta aquí..."
        required
      />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Enviando...' : 'Enviar' }}
      </button>
    </form>
    <div v-if="error" class="error">
      <p>Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>
// Importa la función para obtener la respuesta de ChatGPT
import { getChatResponse } from '../api.js';

export default {
  name: 'Chat',
  data() {
    return {
      userInput: '',
      messages: [], // Mantén un estado inicial vacío
      loading: false,
      error: null,
    };
  },
  mounted() {
    // Cargar mensajes guardados de localStorage si existen
    const savedMessages = localStorage.getItem('chatMessages');
    if (savedMessages) {
      this.messages = JSON.parse(savedMessages);
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    }
  },
  methods: {
    async sendMessage() {
      const question = this.userInput.trim();
      if (question === '') return;

      // Agregar el mensaje del usuario a la conversación
      this.messages.push({ sender: 'user', text: question });

      // Limpiar el input y mostrar el indicador de carga
      this.userInput = '';
      this.loading = true;
      this.error = null;

      // Guardar en localStorage
      this.saveMessages();

      // Desplazar hacia abajo
      this.$nextTick(() => {
        this.scrollToBottom();
      });

      try {
        // Obtener la respuesta de ChatGPT
        const response = await getChatResponse(question);
        // Agregar la respuesta de ChatGPT a la conversación
        this.messages.push({ sender: 'gpt', text: response });

        // Guardar en localStorage
        this.saveMessages();

        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (err) {
        this.error = 'No se pudo obtener una respuesta. Por favor, intenta de nuevo.';
      } finally {
        this.loading = false;
      }
    },
    scrollToBottom() {
      const chatWindow = this.$refs.chatWindow;
      if (chatWindow) {
        chatWindow.scroll({
          top: chatWindow.scrollHeight,
          behavior: 'smooth',
        });
      }
    },
    saveMessages() {
      // Guardar los mensajes en localStorage
      localStorage.setItem('chatMessages', JSON.stringify(this.messages));
    },
     clearChat() {
      // Limpiar el array de mensajes y localStorage
      this.messages = [];
      localStorage.removeItem('chatMessages');
    }
  },
  
};
</script>

<style scoped>
.clear-chat-button {
  background-color: transparent; /* Fondo transparente para el botón */
  color: #f44336; /* Color rojo del ícono */
  border: none;
  font-size: 24px; /* Tamaño del ícono */
  cursor: pointer;
  position: absolute; /* Posicionamos el botón de manera absoluta */
  top: 10px; /* Alineado en la parte superior */
  left: 10px; /* Alineado en la parte izquierda */
}

.clear-chat-button:hover {
  background-color: #d32f2f; /* Color rojo más oscuro al pasar el ratón */
}
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  font-family: 'Poppins', sans-serif;
}

.chat-header {
  background-color: var(--primary-color);
  padding: 15px;
  color: #fff;
  text-align: center;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.chat-window {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #f5f5f5;
  max-height: 400px; /* Limitar el alto máximo */
}

.message {
  margin: 10px 0;
  padding: 10px 15px;
  border-radius: 20px;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user {
  background-color: var(--secondary-color);
  color: #fff;
  align-self: flex-end;
}

.message.gpt {
  background-color: #fffccc;
  border: 1px solid #e0e0e0;
  align-self: flex-start;
}

.input-form {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.input-form input {
  flex: 1;
  padding: 10px 15px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
}

.input-form input:focus {
  border-color: var(--primary-color);
}

.input-form button {
  margin-left: 10px;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background-color: var(--primary-color);
  color: #fff;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.input-form button:hover {
  background-color: var(--secondary-color);
}

.input-form button:disabled {
  background-color: #9E9E9E;
  cursor: not-allowed;
}

.error {
  color: red;
  margin: 10px;
  text-align: center;
}

/* Media query para pantallas pequeñas */
@media (max-width: 600px) {
  .chat-container {
    width: 100%;
    padding: 0;
  }
  .chat-header h2 {
    font-size: 1.2rem;
  }
  .message {
    max-width: 90%;
  }
}
</style>