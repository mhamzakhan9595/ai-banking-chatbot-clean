/**
 * Typing indicator component
 * Shows animated dots while AI is thinking
 */

import React from 'react';
import { Bot } from 'lucide-react';
import './TypingIndicator.css';

const TypingIndicator = () => {
  return (
    <div className="typing-indicator">
      <div className="bubble-avatar">
        <Bot size={20} />
      </div>
      <div className="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
};

export default TypingIndicator;