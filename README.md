# 📄 AI Resume Analyzer

An AI-powered web application that analyzes resumes, evaluates resume quality, matches resumes against job descriptions, and provides personalized AI-powered insights.

The project combines **PDF parsing, rule-based resume analysis, semantic search, vector embeddings, FAISS, and Generative AI** to create an end-to-end resume analysis system.

---

## 🎯 Project Overview

Finding out whether a resume is suitable for a particular job can be difficult for students and job seekers.

This project provides a single platform where users can upload their resume, analyze its structure and skills, compare it with a target job description, and ask an AI assistant questions about their profile.

### The application performs four major tasks:

**1. Resume Analysis**  
Extracts important information and evaluates the structure of the resume.

**2. Skill Analysis**  
Detects technical skills from the resume and job description.

**3. Job Matching**  
Compares resume skills with job requirements and identifies skill gaps.

**4. AI Resume Assistant**  
Uses RAG-based retrieval to provide answers based on the user's resume and target job description.

---

## ✨ Features

### 📄 Resume Parser

Upload a PDF resume and automatically extract:

- Name
- Email
- Phone number
- Technical skills
- Resume sections
- Projects
- Education
- Internships
- Achievements / Activities

### 📊 Resume Scoring

The application evaluates the resume based on important structural elements such as:

- Contact information
- Skills
- Objective / Summary
- Education
- Projects
- Experience / Internships
- Certifications

The analyzer generates a **resume score out of 100** along with improvement suggestions.

### 🎯 Job Description Matching

Paste a job description and compare it with the uploaded resume.

The system provides:

- Required skills
- Matching skills
- Missing skills
- Resume–job match percentage
- Job-specific recommendations

### 🤖 AI Resume Assistant

Users can ask questions such as:

- Why am I a good fit for this role?
- What skills am I missing?
- Which projects are most relevant to this job?
- How does my resume align with this position?

The AI assistant uses information retrieved from the resume and job description to generate contextual responses.

---

# 🧠 AI / RAG Architecture

The AI assistant uses a **Retrieval-Augmented Generation (RAG)** approach.

Instead of relying only on the language model's general knowledge, relevant information is first retrieved from the uploaded resume and job description.

```text
Resume PDF
    │
    ▼
PDF Text Extraction
    │
    ▼
Resume Section Parsing
    │
    ▼
Text Chunking
    │
    ▼
Sentence Transformer
    │
    ▼
Vector Embeddings
    │
    ▼
FAISS Vector Index
    │
    │
    ├──────── User Question
    │                 │
    │                 ▼
    │          Query Embedding
    │                 │
    ▼                 ▼
Relevant Context ◄────┘
    │
    ▼
Hugging Face LLM
    │
    ▼
Contextual AI Response
---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Web Application | Streamlit |
| PDF Processing | pdfplumber |
| Text Processing | Regular Expressions |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| Generative AI | Hugging Face Inference API |
| Numerical Processing | NumPy |
| Version Control | Git, GitHub |

---

## 🏗️ Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py              # Streamlit application
├── parser.py           # Resume PDF parsing
├── analyzer.py         # Resume scoring and JD matching
├── rag.py              # RAG pipeline and AI assistant
├── skills.txt          # Skill vocabulary
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Ignored files and secrets
