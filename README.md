# 🤖 AI Banking Assistant

<div align="center">

**Production-ready AI-powered Banking Chatbot with RAG, Streaming, and Clean Architecture**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **AI Banking Assistant** is a production-ready conversational AI system that provides intelligent banking assistance through:

- **Natural Language Understanding** using Hugging Face LLMs
- **Retrieval-Augmented Generation (RAG)** for document-based Q&A
- **Real-time Streaming** responses like ChatGPT
- **Clean Architecture** with dependency injection
- **Full-stack implementation** with React frontend

---

## ✨ Features

### Core Features
- 🤖 **AI-Powered Chat** - Natural conversations with LLM
- 💬 **Real-time Streaming** - Words appear as generated
- 🧠 **Conversation Memory** - Context-aware responses
- ⚡ **Smart Caching** - 75% cache hit rate for repeated queries
- 🚦 **Rate Limiting** - 10 requests/minute to prevent abuse
- 📝 **Request Logging** - Complete audit trail

### Technical Features
- 🏗️ **Clean Architecture** - Domain-driven design
- 💉 **Dependency Injection** - Loose coupling, testable code
- 🔄 **API Versioning** - Future-proof endpoints
- 🛡️ **Error Handling** - Global exception handlers
- 📊 **Health Checks** - Comprehensive system monitoring
- 🐳 **Docker Ready** - Containerized deployment

### Banking Features (Upcoming)
- 💰 Account balance queries
- 📜 Transaction history
- 💸 Fund transfers
- 📄 Document Q&A (RAG)

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Core language |
| FastAPI | 0.104 | API framework |
| HuggingFace | 4.35 | LLM integration |
| PyTorch | 2.1 | ML runtime |
| Pydantic | 2.5 | Data validation |
| Uvicorn | 0.24 | ASGI server |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18 | UI framework |
| Vite | 5 | Build tool |
| Axios | 1.6 | HTTP client |
| Lucide React | 0.3 | Icons |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| TTLCache | In-memory caching |
| PostgreSQL | User data (coming soon) |
| FAISS | Vector database (coming soon) |
| Docker | Containerization |

---

## 🏗️ Architecture
