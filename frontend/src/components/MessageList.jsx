/**
 * Message list component - scrollable chat history
 */

import React, { useRef, useEffect } from 'react';
import ChatBubble from './ChatBubble';
import TypingIndicator from './TypingIndicator';
import './MessageList.css';

const MessageList = ({ messages, isTyping }) => {
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping]);

  return (
    <div className="message-list" ref={containerRef}>
      {messages.length === 0 ? (
        <div className="welcome-message">
          <h2>🤖 AI Banking Assistant</h2>
          <p>Ask me anything about banking, accounts, or financial questions!</p>
        </div>
      ) : (
        messages.map((message, index) => (
          <ChatBubble key={index} message={message} isUser={message.type === 'user'} />
        ))
      )}
      
      {isTyping && <TypingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;