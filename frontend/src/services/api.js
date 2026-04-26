/**
 * API Service for communicating with backend
 */

const API_BASE_URL = 'http://localhost:8000';

class ChatAPI {
  constructor() {
    this.userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Send message and get response (non-streaming)
   */
  async sendMessage(message, conversationId = null) {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        user_id: this.userId,
        conversation_id: conversationId
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    return response.json();
  }

  /**
   * Send message and stream response token by token
   */
  async sendMessageStream(message, onChunk, onError, onComplete) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          user_id: this.userId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          onComplete && onComplete();
          break;
        }
        
        const chunk = decoder.decode(value);
        onChunk(chunk);
      }
    } catch (error) {
      onError && onError(error.message);
    }
  }

  /**
   * Check backend health
   */
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  }

  /**
   * Get model information
   */
  async getModelInfo() {
    const response = await fetch(`${API_BASE_URL}/api/v1/models/current`);
    return response.json();
  }

  getUserId() {
    return this.userId;
  }
}

export default new ChatAPI();