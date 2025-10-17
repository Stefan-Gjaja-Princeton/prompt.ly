import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, AlertTriangle } from "lucide-react";
import "./ChatWindow.css";

const ChatWindow = ({ messages, onSendMessage, loading, isTerse }) => {
  const [inputMessage, setInputMessage] = useState("");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputMessage.trim() && !loading) {
      onSendMessage(inputMessage.trim());
      setInputMessage("");

      // Reset textarea height after sending
      if (inputRef.current) {
        inputRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);

    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = "auto";
    const newHeight = Math.min(textarea.scrollHeight, 120);
    textarea.style.height = newHeight + "px";

    // If we've reached max height, ensure we can scroll
    if (textarea.scrollHeight > 120) {
      textarea.style.overflowY = "auto";
    } else {
      textarea.style.overflowY = "hidden";
    }
  };

  const handleInputFocus = (e) => {
    // Reset height when focusing
    const textarea = e.target;
    textarea.style.height = "auto";
    const newHeight = Math.min(textarea.scrollHeight, 120);
    textarea.style.height = newHeight + "px";

    // Handle scrolling
    if (textarea.scrollHeight > 120) {
      textarea.style.overflowY = "auto";
    } else {
      textarea.style.overflowY = "hidden";
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-title">
          <Bot size={20} />
          <h2>AI Assistant</h2>
        </div>
        {isTerse && (
          <div className="terse-warning">
            <AlertTriangle size={16} />
            <span>Responses are being limited due to low prompt quality</span>
          </div>
        )}
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <Bot size={48} className="empty-icon" />
            <h3>Start a conversation</h3>
            <p>
              Ask me anything! I'll provide helpful responses and feedback on
              your prompts.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`message ${
                message.role === "user" ? "user-message" : "ai-message"
              }`}
            >
              <div className="message-avatar">
                {message.role === "user" ? (
                  <User size={16} />
                ) : (
                  <Bot size={16} />
                )}
              </div>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                <div className="message-time">
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message ai-message">
            <div className="message-avatar">
              <Bot size={16} />
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            onFocus={handleInputFocus}
            placeholder="Type your message here..."
            className="message-input"
            rows="1"
            disabled={loading}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!inputMessage.trim() || loading}
          >
            <Send size={18} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatWindow;
