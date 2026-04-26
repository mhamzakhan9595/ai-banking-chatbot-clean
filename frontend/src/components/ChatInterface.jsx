/**
 * Main chat interface component
 * Orchestrates all chat components and API communication
 */

import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import ChatAPI from '../services/api';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(true);

  // Check backend connection on mount
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await ChatAPI.healthCheck();
        setIsConnected(true);
      } catch (error) {
        console.error('Backend connection failed:', error);
        setIsConnected(false);
      }
    };
    checkConnection();
  }, []);

  const addMessage = (text, type) => {
    setMessages(prev => [...prev, {
      text: text,
      type: type,
      timestamp: new Date().toISOString()
    }]);
  };
 const clearChat = () => {
    setMessages([]);
};

  const handleSendMessage = async (message) => {
    // Add user message to chat
    addMessage(message, 'user');
    
    // Start typing indicator
    setIsTyping(true);
    
    // Create placeholder for streaming response
    let streamingMessage = '';
    let hasStartedStreaming = false;
    
    try {
      await ChatAPI.sendMessageStream(
        message,
        // onChunk - receive each word/token
        (chunk) => {
          streamingMessage += chunk;
          
          if (!hasStartedStreaming) {
            // First chunk - create AI message placeholder
            setMessages(prev => [...prev, {
              text: streamingMessage,
              type: 'ai',
              timestamp: new Date().toISOString(),
              isStreaming: true
            }]);
            hasStartedStreaming = true;
          } else {
            // Update the last message with new content
            setMessages(prev => {
              const newMessages = [...prev];
              const lastIndex = newMessages.length - 1;
              if (lastIndex >= 0 && newMessages[lastIndex].type === 'ai') {
                newMessages[lastIndex] = {
                  ...newMessages[lastIndex],
                  text: streamingMessage
                };
              }
              return newMessages;
            });
          }
        },
        // onError
        (error) => {
          console.error('Stream error:', error);
          const errorMessage = streamingMessage || `Error: ${error}`;
          if (hasStartedStreaming) {
            setMessages(prev => {
              const newMessages = [...prev];
              const lastIndex = newMessages.length - 1;
              if (lastIndex >= 0 && newMessages[lastIndex].type === 'ai') {
                newMessages[lastIndex] = {
                  ...newMessages[lastIndex],
                  text: errorMessage
                };
              }
              return newMessages;
            });
          } else {
            addMessage(errorMessage, 'ai');
          }
          setIsTyping(false);
        },
        // onComplete
        () => {
          setIsTyping(false);
          // Mark message as complete (remove streaming flag)
          setMessages(prev => {
            const newMessages = [...prev];
            const lastIndex = newMessages.length - 1;
            if (lastIndex >= 0 && newMessages[lastIndex].type === 'ai') {
              const { isStreaming, ...messageWithoutStreaming } = newMessages[lastIndex];
              newMessages[lastIndex] = messageWithoutStreaming;
            }
            return newMessages;
          });
        }
      );
    } catch (error) {
      console.error('Send message error:', error);
      addMessage(`Sorry, I encountered an error: ${error.message}`, 'ai');
      setIsTyping(false);
    }
  };

  if (!isConnected) {
    return (
      <div className="error-container">
        <div className="error-message">
          <h2>🔌 Connection Error</h2>
          <p>Could not connect to the backend server.</p>
          <p>Make sure the backend is running at: http://localhost:8000</p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>🤖 AI Banking Assistant</h1>
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span>Connected</span>
          <button style={{ margin: '0 10px' ,color: 'red' ,background: 'lightgray',padding: '5px 15px',border: '1px solid red' }} onClick={clearChat} className="clear-button">
    Clear Chat
</button>
        </div>
      </div>
     

      <MessageList messages={messages} isTyping={isTyping} />
      <MessageInput onSendMessage={handleSendMessage} disabled={isTyping} />
    </div>
  );
};

export default ChatInterface;