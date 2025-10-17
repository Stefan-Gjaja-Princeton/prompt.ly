import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5001/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const apiService = {
  // Get all conversations
  getConversations: async () => {
    const response = await api.get("/conversations");
    return response.data;
  },

  // Create a new conversation
  createConversation: async () => {
    const response = await api.post("/conversations");
    return response.data;
  },

  // Get a specific conversation
  getConversation: async (conversationId) => {
    const response = await api.get(`/conversations/${conversationId}`);
    return response.data;
  },

  // Send a message to a conversation
  sendMessage: async (conversationId, message) => {
    const response = await api.post(
      `/conversations/${conversationId}/messages`,
      {
        message: message,
      }
    );
    return response.data;
  },

  getAIResponse: async (conversationId) => {
    const response = await api.post(
      `/conversations/${conversationId}/response`
    );
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get("/health");
    return response.data;
  },
};
