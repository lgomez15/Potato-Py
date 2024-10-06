<!-- frontend/src/components/Chat.vue -->
<template>
    <div class="chat-container">
      <h2>Chat con GPT</h2>
      <div class="chat-window">
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
  import { getChatResponse } from '../api.js'; // Ruta correcta// Asegúrate de que la ruta es correcta y usa mayúsculas si es necesario
  
  export default {
    name: 'Chat',
    data() {
      return {
        userInput: '',
        messages: [],
        loading: false,
        error: null,
      };
    },
    methods: {
      async sendMessage() {
        const question = this.userInput.trim();
        if (question === '') return;
  
        // Agrega el mensaje del usuario a la conversación
        this.messages.push({ sender: 'user', text: question });
  
        // Limpia el input y muestra el indicador de carga
        this.userInput = '';
        this.loading = true;
        this.error = null;
  
        try {
          // Obtiene la respuesta de ChatGPT
          const response = await getChatResponse(question);
          // Agrega la respuesta de ChatGPT a la conversación
          this.messages.push({ sender: 'gpt', text: response });
        } catch (err) {
          this.error = 'No se pudo obtener una respuesta. Por favor, intenta de nuevo.';
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .chat-window {
    border: 1px solid #ccc;
    padding: 10px;
    height: 400px;
    overflow-y: auto;
    background-color: #f9f9f9;
    margin-bottom: 10px;
  }
  
  .message {
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
    max-width: 80%;
  }
  
  .message.user {
    background-color: #d1e7dd;
    align-self: flex-end;
    margin-left: auto;
  }
  
  .message.gpt {
    background-color: #f8d7da;
    align-self: flex-start;
    margin-right: auto;
  }
  
  .input-form {
    display: flex;
  }
  
  .input-form input {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .input-form button {
    padding: 10px 20px;
    font-size: 16px;
    margin-left: 10px;
    border: none;
    background-color: #4CAF50;
    color: white;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .input-form button:disabled {
    background-color: #9E9E9E;
    cursor: not-allowed;
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  