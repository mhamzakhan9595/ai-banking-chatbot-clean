/**
 * Message input component with send button
 */

import React, { useState } from 'react';
import { Send } from 'lucide-react';
import './MessageInput.css';

const MessageInput = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      <textarea
        className="message-input"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        disabled={disabled}
        rows={1}
      />
      <button 
        type="submit" 
        className="send-button"
        disabled={disabled || !input.trim()}
      >
        <Send size={20} />
      </button>
    </form>
  );
};

export default MessageInput;