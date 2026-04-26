# 🤖 AI Banking Assistant

## Production-ready AI-powered banking chatbot with LLM, RAG, and API integration.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co)

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

---

## Overview

The **AI Banking Assistant** is a full-stack application that provides intelligent conversational capabilities for banking operations. It uses state-of-the-art language models to understand user queries, retrieve relevant information from documents (RAG), and interact with banking APIs.

### Key Capabilities

- **Natural Language Conversations** - Powered by Hugging Face LLMs
- **Document Q&A** - RAG implementation for banking documents
- **API Integration** - Function calling for banking operations
- **Chat History** - Persistent conversation storage
- **Authentication** - JWT-based secure access
- **Production Ready** - Docker, rate limiting, caching

---

## Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11.9 | Core language |
| FastAPI | 0.104.1 | Web framework |
| Hugging Face Transformers | 4.35.0 | LLM integration |
| PyTorch | 2.1.0 | ML runtime |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI framework |
| Vite | 5.x | Build tool |
| Axios | Latest | HTTP client |
| Lucide React | Latest | Icons |

### Infrastructure

| Technology | Purpose |
|------------|---------|
| PostgreSQL | Structured data (Coming) |
| FAISS/Chroma | Vector database (Coming) |
| Docker | Containerization |
| Redis | Caching (Optional) |

---

## Features

### Completed (Days 1-6)

#### Day 1-2: Core AI & Backend
- FastAPI server with CORS
- Hugging Face DialoGPT-small integration
- Conversation memory and context
- Error handling and logging

#### Day 3: Production Enhancements
- Response streaming (real-time typing)
- Rate limiting (10 requests/minute)
- Response caching (TTL-based)
- Multiple model support
- Structured logging

#### Day 4: Clean Architecture
- Domain-driven design
- Dependency injection
- Repository pattern
- Interface-based design
- Global error handlers

#### Day 5-6: Frontend & Integration
- React + Vite setup
- Chat UI components
- Streaming response display
- Typing indicator
- Full-stack integration

### In Progress (Days 7-14)

- Day 7: GitHub & Documentation
- Day 8: RAG Setup (Document processing)
- Day 9: Vector Database (FAISS/Chroma)
- Day 10: RAG Integration
- Day 11: PostgreSQL & Chat History
- Day 12: Authentication (JWT)
- Day 13: Function Calling (Banking APIs)
- Day 14: Docker Deployment

---

### Project Structure

```mermaid
graph TD
    A[AI Banking Chatbot]

    A --> B[Backend]
    A --> C[Frontend]

    B --> B1[app]
    B1 --> B2[api]
    B2 --> B3[middlewares]
    B2 --> B4[v1]
    B4 --> B5[chat.py]
    B4 --> B6[health.py]
    B4 --> B7[models.py]

    B1 --> B8[core]
    B1 --> B9[domain]
    B1 --> B10[infrastructure]
    B1 --> B11[schemas]
    B1 --> B12[main.py]

    B9 --> D1[entities/chat.py]
    B9 --> D2[interfaces]
    B9 --> D3[services]

    B10 --> E1[cache]
    B10 --> E2[llm]
    B10 --> E3[rate_limit]

    C --> C1[src]
    C1 --> C2[components]
    C1 --> C3[services]
    C1 --> C4[App.jsx]
    C1 --> C5[main.jsx]

    
---

## Installation

### Prerequisites

- Python 3.11+ (Download from python.org)
- Node.js 18+ (Download from nodejs.org)
- Git (Download from git-scm.com)
- 8GB RAM minimum (16GB recommended for larger models)

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-banking-chatbot.git
cd ai-banking-chatbot

# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000