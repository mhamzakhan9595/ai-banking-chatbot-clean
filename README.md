# 🤖 AI Banking Assistant

## Production-ready AI-powered banking chatbot with LLM, RAG, and API integration

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co)

---

## 📚 Table of Contents

* [Overview](#overview)
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [API Documentation](#api-documentation)
* [Future Improvements](#future-improvements)

---

## 📌 Overview

The **AI Banking Assistant** is a full-stack application that enables intelligent conversations for banking operations using LLMs and RAG.

### 🚀 Key Capabilities

* Natural language conversations
* Document-based Q&A (RAG)
* API integration
* Chat memory & context
* Scalable backend architecture

---

## 🛠 Tech Stack

### Backend

* Python 3.11
* FastAPI
* Hugging Face Transformers
* PyTorch

### Frontend

* React
* Vite
* Axios

### Infrastructure

* Docker
* Redis (optional)
* PostgreSQL (planned)
* FAISS / Chroma (planned)

---

## ✨ Features

### ✅ Completed

* FastAPI backend
* LLM integration
* Chat UI (React)
* Streaming responses
* Rate limiting + caching

### 🚧 In Progress

* RAG pipeline
* Vector DB
* Authentication
* Deployment

---

## 🗂 Project Structure (Mermaid Diagram)

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

    B9 --> D1[entities]
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
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.11+
* Node.js 18+
* Git

---

### 🔧 Backend Setup

```bash
git clone https://github.com/yourusername/ai-banking-chatbot.git
cd ai-banking-chatbot/backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## ▶️ Running the Application

* Backend → http://localhost:8000
* Frontend → http://localhost:5173

---

## 📡 API Documentation

* Swagger → http://localhost:8000/docs
* ReDoc → http://localhost:8000/redoc

---

## 🚀 Future Improvements

* Full RAG system
* Authentication (JWT)
* Chat history persistence
* Docker deployment
* Model optimization

---

## 📄 License

For educational and portfolio use.
