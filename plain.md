# LexGuard — AI Rights & Contract Intelligence System

## Overview
LexGuard is an AI-powered contract intelligence platform designed to analyze legal and quasi-legal documents before users agree to them.

The system helps users:
- Detect hidden legal risks
- Understand complex clauses
- Identify exploitative terms
- Generate safer negotiation alternatives
- Ask AI questions regarding uploaded contracts

---

# Core Features

## Authentication
### Firebase Authentication
- Google Login
- Email & Password Login

### Firestore
Store:
- user profiles
- uploaded contracts
- previous legal conversations
- analysis history
- chatbot history

---

# Contract Processing Pipeline

```text
Upload Contract
      ↓
OCR + Parsing
      ↓
Clause Extraction
      ↓
Clause Classification
      ↓
Risk Detection
      ↓
AI Legal Reasoning
      ↓
Negotiation Suggestions
      ↓
Dashboard + Chatbot
```

---

# OCR & Parsing

## Supported Formats
- PDF
- DOCX
- Scanned Documents

## Tools
- PyMuPDF
- pdfplumber
- PaddleOCR

---

# Clause Extraction Engine

Extract important clauses such as:
- Non-compete
- Arbitration
- Intellectual Property
- Privacy
- Payment
- Termination
- Liability

---

# AI Agents

## 1. Clause Extraction Agent
Extracts structured legal clauses.

## 2. Risk Analysis Agent
Detects:
- hidden liabilities
- exploitative conditions
- penalties
- risky obligations

## 3. Explanation Agent
Converts legal text into simple language.

## 4. Negotiation Agent
Suggests:
- safer alternatives
- counter offers
- negotiation points

---

# AI Chatbot

## Purpose
Users can ask questions related to uploaded contracts.

Examples:
- "Can they terminate me without notice?"
- "Is this clause dangerous?"
- "Can the company own my side projects?"

---

# Chatbot Workflow

```text
User Question
      ↓
Retrieve Relevant Clauses
      ↓
RAG Search
      ↓
Gemini Legal Reasoning
      ↓
Human-Friendly Explanation
```

---

# RAG Architecture

## Why RAG?
Prevents hallucinations and improves grounded legal reasoning.

## Components
### Embeddings
- BGE-large
- E5-large

### Vector Database
- ChromaDB

### Framework
- LangChain

---

# AI Models

## LLM
- Gemini 2.5 Pro
- Gemini Flash

## NLP
- spaCy
- transformers

## Agent Framework
- LangGraph

---

# Recommended Datasets

## CUAD Dataset
Contract Understanding Atticus Dataset.

## LEDGAR
Large legal clause classification dataset.

## Indian Legal References
- labor regulations
- DPDP Act
- compliance policies

---

# Frontend Architecture

## Stack
- Next.js
- Tailwind CSS
- shadcn/ui

## Pattern
MVVM Architecture

```text
UI Layer
   ↓
ViewModel
   ↓
Repository
   ↓
API
```

---

# Backend Architecture

## Stack
- FastAPI
- Python

## Pattern
Clean Architecture

```text
Presentation Layer
        ↓
Service Layer
        ↓
AI Orchestration Layer
        ↓
Repository Layer
        ↓
Database
```

---

# Database Design

## PostgreSQL
Store:
- users
- reports
- contracts
- risks

## Firestore
Store:
- conversations
- user history
- chatbot interactions

## ChromaDB
Store:
- embeddings
- legal references
- benchmark clauses

---

# Risk Categories

## Employment Risks
- non-compete
- forced arbitration
- immediate termination

## Financial Risks
- hidden penalties
- auto renewals
- cancellation charges

## Privacy Risks
- excessive data collection

## Intellectual Property Risks
- ownership transfer

---

# Core Screens

## 1. Login Screen
- Google Login
- Email Login

## 2. Dashboard
- contract history
- risk score
- analysis reports

## 3. Clause Explorer
- highlighted risky clauses
- categorized sections

## 4. AI Legal Chat Screen
- contextual chatbot
- legal explanations
- negotiation help

## 5. Risk Analysis Screen
- severity indicators
- implications
- recommendations

---

# Deployment

## Frontend
- Vercel

## Backend
- Railway / Render

## Database
- Supabase PostgreSQL

---

# Final Product Vision

LexGuard is not just a contract summarizer.

It is an AI-powered contract defense system designed to protect users before they sign legal agreements.

