import React, { useState, useEffect, useCallback } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "./App.css";
import ConversationList from "./components/ConversationList";
import ChatWindow from "./components/ChatWindow";
import FeedbackPanel from "./components/FeedbackPanel";
import UserHeader from "./components/UserHeader";
import LoginPage from "./components/LoginPage";
import { createApiService } from "./services/apiService";

function App() {
  const { isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();
  const apiService = createApiService(getAccessTokenSilently);
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [qualityScore, setQualityScore] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [isTerse, setIsTerse] = useState(false);
  const [loading, setLoading] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const loadConversations = useCallback(async () => {
    try {
      const data = await apiService.getConversations();
      setConversations(data);
    } catch (error) {
      console.error("Error loading conversations:", error);
    }
  }, [apiService]);

  const loadConversation = useCallback(
    async (conversationId) => {
      try {
        const data = await apiService.getConversation(conversationId);
        setMessages(data.messages || []);
        setQualityScore(data.quality_score);
        setIsTerse(data.quality_score !== null && data.quality_score <= 5.0);
      } catch (error) {
        console.error("Error loading conversation:", error);
      }
    },
    [apiService]
  );

  // Load conversations on app start (component mount)
  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  // Ensure conversations load as soon as the user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadConversations();
    }
  }, [isAuthenticated, loadConversations]);

  // Load conversation when currentConversationId changes
  useEffect(() => {
    if (currentConversationId) {
      loadConversation(currentConversationId);
    }
  }, [currentConversationId, loadConversation]);

  const createNewConversation = async () => {
    try {
      const data = await apiService.createConversation();
      const newConversation = {
        conversation_id: data.conversation_id,
        title: "New Conversation",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        message_count: 0,
      };

      setConversations((prev) => [newConversation, ...prev]);
      setCurrentConversationId(data.conversation_id);
      setMessages([]);
      setQualityScore(null);
      setFeedback("");
      setIsTerse(false);

      return data.conversation_id;
    } catch (error) {
      console.error("Error creating conversation:", error);
      throw error;
    }
  };

  const sendMessage = async (message) => {
    // Ensure we have a conversation to send into; create one if needed
    let activeConversationId = currentConversationId;
    if (!activeConversationId) {
      try {
        activeConversationId = await createNewConversation();
      } catch (e) {
        alert(`Error creating conversation: ${e.message || e}`);
        return;
      }
    }

    // Add user message immediately to the chat
    const userMessage = {
      role: "user",
      content: message,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);
    setFeedbackLoading(true);
    try {
      // Step 1: Get feedback and score immediately
      const feedbackResponse = await apiService.sendMessage(
        activeConversationId,
        message
      );

      console.log("DEBUG: Feedback Response:", feedbackResponse);

      // Update feedback and score immediately
      setQualityScore(feedbackResponse.quality_score);
      setFeedback(feedbackResponse.feedback);
      setIsTerse(
        feedbackResponse.quality_score !== null &&
          feedbackResponse.quality_score <= 5.0
      );

      // Stop feedback loading immediately
      setFeedbackLoading(false);

      // Step 2: Get AI response after feedback is ready
      const aiResponse = await apiService.getAIResponse(activeConversationId);

      console.log("DEBUG: AI Response:", aiResponse);

      // Update with the complete message history including AI response
      setMessages(aiResponse.messages);

      // Update conversations list
      loadConversations();
    } catch (error) {
      console.error("Error sending message:", error);
      // Show error message to user
      alert(`Error sending message: ${error.message || error}`);
      // Remove the user message if there was an error
      setMessages((prev) => prev.filter((msg) => msg !== userMessage));
    } finally {
      setLoading(false);
    }
  };

  const selectConversation = (conversationId) => {
    setCurrentConversationId(conversationId);
  };

  if (isLoading) {
    return <div className="app">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <div className="app">
      <UserHeader />
      <div className="app-container">
        <ConversationList
          conversations={conversations}
          currentConversationId={currentConversationId}
          onSelectConversation={selectConversation}
          onCreateNew={createNewConversation}
        />

        <ChatWindow
          messages={messages}
          onSendMessage={sendMessage}
          loading={loading}
          isTerse={isTerse}
        />

        <FeedbackPanel
          qualityScore={qualityScore}
          feedback={feedback}
          isTerse={isTerse}
          loading={feedbackLoading}
        />
      </div>
    </div>
  );
}

export default App;
