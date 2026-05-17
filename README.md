# ⚖️ LexGuard — Multi-Agent AI Contract Intelligence System

LexGuard is an advanced, production-grade legal intelligence platform designed to scan terms of service, NDAs, and contracts for potential hazards. Powered by Google's Gemini models and structured around a concurrent Multi-Agent architecture, LexGuard automatically highlights critical risks, grades contract terms, and provides an interactive conversational sandbox where users can ask specific legal questions about their documents.

---

## 🚀 Key Features

*   **📂 Multi-Source Document Ingestion:** Input raw contract text or directly upload **PDF files**. The backend automatically parses and runs optical text extraction.
*   **🤖 Multi-Agent Risk Assessments:** An asynchronous analysis pipeline that processes documents in parallel across three specialized AI agents:
    *   **💰 Financial Risk Agent:** Scrutinizes fee structures, auto-renewals, unexpected liabilities, and payment obligations.
    *   **⚖️ Legal & Liability Agent:** Analyzes indemnification clauses, governing laws, arbitration mandates, and termination options.
    *   **🔒 Privacy & Data Security Agent:** Dissects data retention policies, third-party transfers, and intellectual property handovers.
*   **💬 Conversational Contract Chatbot:** Ask precise questions about the document in an interactive sandbox. The system generates contextual, grounded answers directly from the contract text.
*   **🔒 Protected User Workspaces:** Integrated securely with Firebase Authentication, preventing unauthorized access and securing user sessions.

---

## 🏛️ Architectural Overview

LexGuard is built using state-of-the-art software patterns to maximize testability, separation of concerns, and codebase maintainability:

```
                  ┌───────────────────────────────────────────────┐
                  │            LexGuard Next.js Web App           │
                  │              (Frontend / MVVM)                │
                  └───────────────────────┬───────────────────────┘
                                          │  API Uploads / Queries
                                          ▼
                  ┌───────────────────────────────────────────────┐
                  │             FastAPI Web Server                │
                  │             (Backend Gateway)                 │
                  └───────────────────────┬───────────────────────┘
                                          │  OCR / Service Routing
                                          ▼
                  ┌───────────────────────────────────────────────┐
                  │          Analysis Service Orchestrator        │
                  │            (Concurrent Agent Engine)          │
                  └──────┬────────────────┬────────────────┬──────┘
                         │                │                │
                         ▼                ▼                ▼
                  ┌────────────┐   ┌────────────┐   ┌────────────┐
                  │ Financial  │   │ Legal/Liab │   │ Privacy/IP │
                  │  AI Agent  │   │  AI Agent  │   │  AI Agent  │
                  └──────┬─────┘   └─────┬──────┘   └─────┬──────┘
                         │               │                │
                         └───────────────┼────────────────┘
                                         ▼ (async gather)
                  ┌───────────────────────────────────────────────┐
                  │          Google Gemini API Integration        │
                  └───────────────────────────────────────────────┘
```

### 📂 Directory Map
*   `/frontend` - Build on Next.js 14 utilizing the Model-View-ViewModel (MVVM) architecture pattern.
    *   `/src/app` - Routing and premium dashboard screens (App Router).
    *   `/src/viewmodels` - Decoupled presentation logic (Auth, Risk Analysis, Chat State).
*   `/backend` - Powered by FastAPI, following a strict Clean Architecture pattern.
    *   `/app/api` - REST request/response controllers and endpoints.
    *   `/app/services` - Business core layer orchestrating text extraction and agent gather routines.
    *   `/app/ai_orchestration` - Dedicated Gemini client containing role-based AI system prompts.

---

## 🛠️ Setup & Local Installation

### 1. Prerequisite Environments
Create configuration files in both root workspaces before booting the ecosystem.

*   **Backend Environment (`/backend/.env`):**
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    PORT=8000
    ```

*   **Frontend Environment (`/frontend/.env.local`):**
    ```env
    NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
    NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
    NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_firebase_project_id
    NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
    NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
    NEXT_PUBLIC_FIREBASE_APP_ID=your_firebase_app_id
    NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id
    ```

---

### 2. Booting the Python Backend
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Set up virtual environment and install requirements:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```
3. Boot the FastAPI web server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *The Swagger interactive documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs)*

---

### 3. Booting the Next.js Frontend
1. Open a new terminal tab/window and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Run the hot-reloading development server:
   ```bash
   npm run dev
   ```
   *Open [http://localhost:3000](http://localhost:3000) inside your browser to access the LexGuard Workspace!*

---

## 🛡️ License & Attributions
LexGuard is developed for commercial-grade legal risk assessments. Made with ❤️ using **Google Gemini Pro**, **Next.js**, and **FastAPI**.
