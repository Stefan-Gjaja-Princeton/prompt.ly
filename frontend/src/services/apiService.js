import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5001/api";

// Create API service factory that accepts token getter
export const createApiService = (getAccessTokenSilently) => {
  const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Add interceptor to include auth token
  api.interceptors.request.use(
    async (config) => {
      try {
        const token = await getAccessTokenSilently();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error("Error getting token:", error);
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  return {
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
};

// Default export for compatibility (won't include auth)
export const apiService = {
  getConversations: async () => {
    const response = await axios.get(`${API_BASE_URL}/conversations`);
    return response.data;
  },
  createConversation: async () => {
    const response = await axios.post(`${API_BASE_URL}/conversations`);
    return response.data;
  },
  getConversation: async (conversationId) => {
    const response = await axios.get(
      `${API_BASE_URL}/conversations/${conversationId}`
    );
    return response.data;
  },
  sendMessage: async (conversationId, message) => {
    const response = await axios.post(
      `${API_BASE_URL}/conversations/${conversationId}/messages`,
      { message }
    );
    return response.data;
  },
  getAIResponse: async (conversationId) => {
    const response = await axios.post(
      `${API_BASE_URL}/conversations/${conversationId}/response`
    );
    return response.data;
  },
  healthCheck: async () => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },
};
