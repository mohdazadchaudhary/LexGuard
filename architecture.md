# LexGuard Architecture

## System Overview
LexGuard is an AI-powered contract intelligence platform. It uses a separated frontend and backend architecture to ensure scalability, maintainability, and clean separation of concerns.

## Architecture Patterns

### Frontend: MVVM (Model-View-ViewModel)
- **View (UI Layer):** React Components (Next.js 14). Responsible only for rendering UI and forwarding user events to the ViewModel.
- **ViewModel (Presentation Logic):** Custom React Hooks (e.g., `useAuthViewModel`). Manages state, handles user interactions, and communicates with the Models/Services.
- **Model (Data/Service Layer):** API clients, Firebase SDK wrappers, and data interfaces.

### Backend: Clean Architecture
- **Presentation Layer (API):** FastAPI routers and endpoints (`app/api/`). Handles HTTP requests and responses.
- **Business Logic Layer (Use Cases):** Core application logic (`app/services/` and `app/ai_orchestration/`). Orchestrates tasks like document extraction and AI analysis.
- **Data Access Layer (Repositories):** Interfaces for database interactions (`app/repositories/`).
- **Infrastructure Layer:** Concrete implementations of external services, databases (Firestore/PostgreSQL), and AI providers (e.g., Groq, Gemini).

## Folder Structure

### Frontend (`/frontend`)
- `src/app/`: Next.js App Router pages and layouts (Views).
- `src/components/`: Reusable UI components.
- `src/viewmodels/`: React hooks containing presentation logic and state management.
- `src/models/`: TypeScript interfaces and domain models.
- `src/services/`: API clients and external service integrations.
- `src/lib/`: Configuration files (e.g., Firebase).

### Backend (`/backend`)
- `app/api/`: FastAPI routers and dependency injection.
- `app/core/`: Application config, security, and constants.
- `app/services/`: Business logic and use cases.
- `app/ai_orchestration/`: AI/LLM integration and prompt management.
- `app/repositories/`: Database access patterns.
- `app/models/`: Pydantic schemas and database models.

## Data Flow (Example: Document Analysis)
1. **User** uploads a document via the **Frontend View**.
2. **ViewModel** handles the file state and calls the **Frontend Service**.
3. **Frontend Service** sends an HTTP POST request to the **Backend API**.
4. **Backend API** validates the request and calls the **Document Analysis Service**.
5. **Document Analysis Service** delegates OCR to an external tool, then calls the **AI Orchestration Layer**.
6. **AI Orchestration Layer** communicates with the chosen LLM (e.g., Groq, Gemini) to analyze clauses.
7. Results are saved via the **Repository** and returned back through the layers to the **ViewModel**, which updates the **View**.

## Key Decisions & Workflows
- **Authentication:** Managed via Firebase Auth on the client, with token verification on the backend.
- **Multi-Agent Approach:** Work is strictly divided into Frontend (Views/ViewModels), Backend (API/Services), and AI (Orchestration/LLM models).
