// api.js
import OpenAI from "openai";

// Inicializa OpenAI con tu clave API
const openai = new OpenAI({
  apiKey: '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', // Reemplaza con tu propia clave API
  dangerouslyAllowBrowser: true, // ⚠️ Riesgo: Exponer la clave API en el frontend
});

/**
 * Función para obtener la respuesta de ChatGPT
 * @param {string} userQuestion - La pregunta del usuario
 * @returns {Promise<string>} - La respuesta generada por ChatGPT
 */
export const getChatResponse = async (userQuestion) => {
  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Eres un agricultor" },
        { role: "user", content: userQuestion },
      ],
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Error al obtener la respuesta de ChatGPT:', error);
    throw error;
  }
};
