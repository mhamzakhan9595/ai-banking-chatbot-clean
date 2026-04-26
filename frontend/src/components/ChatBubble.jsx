/**
 * Individual chat bubble component
 * Shows user or AI message with styling
 */

import React from 'react';
import { Bot, User } from 'lucide-react';
import './ChatBubble.css';

const ChatBubble = ({ message, isUser }) => {
  const formattedTime = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`chat-bubble ${isUser ? 'user' : 'ai'}`}>
      <div className="bubble-avatar">
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      <div className="bubble-content">
        <div className="bubble-text">{message.text}</div>
        <div className="bubble-time">{formattedTime}</div>
      </div>
    </div>
  );
};

export default ChatBubble;