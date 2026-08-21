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

The AI assistant retrieves relevant information from the resume and job description to generate contextual responses.

---

## 🧠 AI / RAG Architecture

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
```

### RAG Process

1. Extract text from the uploaded resume.
2. Organize the resume into sections.
3. Create text chunks from the resume and job description.
4. Generate vector embeddings using Sentence Transformers.
5. Store the embeddings in a FAISS vector index.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant information.
8. Provide the retrieved context to the language model.
9. Generate the final contextual AI response.

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
```

### File Responsibilities

**`app.py`**

Handles the Streamlit interface and connects the resume parser, analyzer, job matching system, and AI assistant.

**`parser.py`**

Extracts resume text, contact information, skills, and resume sections from PDF files.

**`analyzer.py`**

Handles:

- Resume scoring
- Job-description skill extraction
- Skill comparison
- Match percentage
- Improvement suggestions

**`rag.py`**

Implements the RAG pipeline using:

- Sentence Transformers
- FAISS
- Hugging Face Inference API
- Retrieved resume and job-description context

**`skills.txt`**

Contains the predefined skill vocabulary used for skill detection.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/sania248/AI-Resume-Analyzer.git
```

Navigate to the project directory:

```bash
cd AI-Resume-Analyzer
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Hugging Face Configuration

The AI Resume Assistant requires a Hugging Face access token.

The token should be stored as an environment variable instead of being written directly in the source code.

### Windows PowerShell

```powershell
$env:HF_TOKEN="your_hugging_face_token"
```

> ⚠️ Never commit API keys, access tokens, `.env` files, or other sensitive credentials to GitHub.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔄 Application Workflow

```text
Upload Resume
      ↓
Extract Resume Information
      ↓
Detect Skills & Sections
      ↓
Calculate Resume Score
      ↓
View Improvement Suggestions
      ↓
Paste Job Description
      ↓
Extract Required Skills
      ↓
Compare Resume & Job
      ↓
View Matching / Missing Skills
      ↓
Ask AI Assistant
      ↓
Retrieve Relevant Context
      ↓
Generate AI Response
```

---

## 💡 What I Learned

This project helped me gain practical experience in building an end-to-end AI-powered application.

Key learnings include:

- **PDF Processing:** Learned how to extract and process text from resume PDF documents using `pdfplumber`.
- **Text Processing:** Used Python regular expressions to identify and extract structured information such as names, email addresses, phone numbers, and technical skills.
- **Resume Analysis:** Learned how to design rule-based scoring logic to evaluate resume completeness and provide improvement suggestions.
- **Job Description Analysis:** Implemented skill extraction from job descriptions and compared required skills with the skills detected in a resume.
- **Semantic Search:** Learned how text can be converted into numerical representations using sentence embeddings for similarity-based retrieval.
- **Vector Search:** Gained practical experience using FAISS to store and retrieve relevant vector embeddings.
- **RAG Architecture:** Learned how Retrieval-Augmented Generation combines information retrieval with a language model to generate responses based on user-provided context.
- **Generative AI Integration:** Integrated the Hugging Face Inference API to generate contextual responses using retrieved information.
- **Streamlit Development:** Learned how to build an interactive web application and connect multiple Python modules through a Streamlit interface.
- **Application Security:** Learned the importance of keeping API keys and sensitive configuration outside the source code.
- **Version Control:** Gained hands-on experience using Git and GitHub to manage and document a software project.

---

## 🔮 Future Improvements

The current application provides resume analysis, skill-based job matching, and a RAG-powered AI assistant. The following improvements could make the system more comprehensive:

- **ATS Compatibility Analysis:** Evaluate resume formatting, section structure, keyword usage, and other factors that can affect Applicant Tracking System compatibility.
- **Semantic Resume–Job Matching:** Enhance the current skill-based matching system by using embeddings to measure semantic similarity between the resume and job description.
- **DOCX Support:** Allow users to upload and analyze Word (`.docx`) resumes in addition to PDF files.
- **Improved Resume Recommendations:** Provide more detailed and role-specific suggestions for improving resume content, skills, projects, and descriptions.
- **Multiple Job Comparison:** Allow users to compare one resume against multiple job descriptions and identify the roles with the highest compatibility.
- **Resume Report Generation:** Generate a downloadable report containing the resume score, matched skills, missing skills, and AI-generated recommendations.
- **Cloud Deployment:** Deploy the application to a cloud platform so users can access it without running the project locally.
- **Enhanced AI Reliability:** Add support for multiple LLM providers or fallback models to improve availability when an AI service is temporarily unavailable.
- **User Authentication and History:** Allow users to securely save their resume analyses and review previous job-matching results.

---

## 👩‍💻 Author

**Sania Begum Shaik**

Artificial Intelligence & Data Science Undergraduate

GitHub: [Sania Begum Shaik](https://github.com/sania248)
