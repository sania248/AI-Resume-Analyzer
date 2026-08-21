# 📄 AI Resume Analyzer

An AI-powered resume analysis application that helps candidates understand how well their resume matches a specific job description.

The application extracts structured information from a resume, evaluates its overall quality, identifies technical skills, compares those skills with job requirements, and uses a Retrieval-Augmented Generation (RAG) pipeline to provide contextual AI-powered insights.

---

## 🎯 About the Project

Job seekers often struggle to understand whether their resume is relevant to a particular job and which skills they need to improve.

The **AI Resume Analyzer** addresses this problem by combining traditional resume parsing, rule-based analysis, semantic search, and generative AI into a single application.

A user can upload a PDF resume and receive:

- Resume information and detected skills
- A resume quality score
- Structured resume sections
- Resume improvement suggestions
- Job-specific skill matching
- Matching and missing skills
- Resume–job match percentage
- AI-generated answers about their suitability for a role

The project demonstrates how **NLP, vector embeddings, information retrieval, and generative AI** can be combined to build a practical career-assistance application.

---

## 🚀 Key Features

### 📄 Resume Parsing

- Upload a resume in PDF format
- Extract resume text using `pdfplumber`
- Detect candidate name, email, and phone number
- Identify technical skills
- Detect and organize resume sections such as:
  - Objective
  - Education
  - Projects
  - Internships
  - Technical Skills
  - Achievements / Activities

### 📊 Resume Quality Analysis

The application evaluates the structure of the resume based on:

- Contact information
- Technical skills
- Objective / summary
- Education
- Projects
- Experience / internships
- Certifications

It generates an overall score out of 100 and provides improvement suggestions.

### 🎯 Job Description Matching

Users can paste a job description to compare it against their resume.

The system identifies:

- Required skills
- Matching skills
- Missing skills
- Resume–job match percentage
- Job-specific recommendations

### 🤖 AI Resume Assistant

The application includes an AI assistant that allows users to ask questions such as:

> "Why am I a good fit for this job?"

> "What skills am I missing for this role?"

> "Which projects in my resume are most relevant to this position?"

The assistant generates responses using the resume and job description as contextual information.

---

## 🧠 Retrieval-Augmented Generation (RAG)

One of the main technical components of the project is the RAG pipeline used by the AI Resume Assistant.

Instead of directly sending the entire resume to the language model, the application:

1. Extracts the resume content
2. Organizes the information into meaningful sections
3. Creates text chunks from the resume and job description
4. Converts the chunks into vector embeddings
5. Stores the embeddings in a FAISS index
6. Converts the user's question into an embedding
7. Retrieves the most relevant resume/job information
8. Provides the retrieved context to the language model
9. Generates a contextual answer

### RAG Architecture

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
            Text Chunks
                 │
                 ▼
       Sentence Transformer
                 │
                 ▼
           Vector Embeddings
                 │
                 ▼
              FAISS
          Vector Database
                 │
                 │
       User Question
                 │
                 ▼
        Query Embedding
                 │
                 ▼
       Relevant Context
          Retrieval
                 │
                 ▼
        Hugging Face LLM
                 │
                 ▼
          AI Response
