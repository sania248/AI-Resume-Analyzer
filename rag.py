import os
import re

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient


# ==================================================
# CONFIGURATION
# ==================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"


# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        _embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _embedding_model


# ==================================================
# GET HUGGING FACE TOKEN
# ==================================================

def get_hf_token():

    # Local development
    token = os.getenv("HF_TOKEN")

    if token:
        return token

    # Streamlit deployment
    try:

        import streamlit as st

        if "HF_TOKEN" in st.secrets:
            return st.secrets["HF_TOKEN"]

    except Exception:
        pass

    return None


# ==================================================
# CLEAN TEXT
# ==================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==================================================
# CREATE RESUME CHUNKS
# ==================================================

def create_chunks(text, sections=None):

    chunks = []

    # ==================================================
    # USE STRUCTURED RESUME SECTIONS
    # ==================================================

    if sections:

        for section_name, section_text in sections.items():

            if not section_text:
                continue

            section_text = section_text.strip()

            if len(section_text) < 20:
                continue

            section_lower = section_name.lower()


            # ==================================================
            # PROJECTS
            # ==================================================

            if section_lower == "projects":

                project_blocks = re.split(
                    r"\n(?=[A-Z][^\n]{2,80}\|)",
                    section_text
                )

                # Alternative project separator
                if len(project_blocks) == 1:

                    project_blocks = re.split(
                        r"\n(?=[A-Z][A-Za-z0-9 ]{2,80}\s+-)",
                        section_text
                    )

                for project in project_blocks:

                    project = project.strip()

                    if len(project) > 30:

                        chunks.append(
                            "Resume Section: Projects\n"
                            + clean_text(project)
                        )


            # ==================================================
            # INTERNSHIPS
            # ==================================================

            elif section_lower == "internships":

                chunks.append(
                    "Resume Section: Internships\n"
                    + clean_text(section_text)
                )


            # ==================================================
            # OTHER SECTIONS
            # ==================================================

            else:

                chunks.append(
                    f"Resume Section: "
                    f"{section_name.title()}\n"
                    f"{clean_text(section_text)}"
                )


    # ==================================================
    # FALLBACK TO RAW TEXT
    # ==================================================

    if not chunks and text.strip():

        paragraphs = re.split(
            r"\n\s*\n",
            text
        )

        for paragraph in paragraphs:

            paragraph = clean_text(
                paragraph
            )

            if len(paragraph) > 30:

                chunks.append(
                    paragraph
                )


    # ==================================================
    # FINAL FALLBACK
    # ==================================================

    if not chunks and text.strip():

        chunks = [

            text[i:i + 800]

            for i in range(
                0,
                len(text),
                700
            )

        ]


    return chunks


# ==================================================
# BUILD FAISS INDEX
# ==================================================

def build_vector_index(chunks):

    if not chunks:
        return None, None

    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype(
        "float32"
    )

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(
        embeddings
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    return index, embeddings


# ==================================================
# RETRIEVE RELEVANT CHUNKS
# ==================================================

def retrieve_chunks(
    query,
    chunks,
    index,
    top_k=5
):

    if not chunks or index is None:
        return []

    model = get_embedding_model()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    faiss.normalize_L2(
        query_embedding
    )

    k = min(
        top_k,
        len(chunks)
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx >= 0:

            results.append(
                {
                    "text": chunks[idx],
                    "score": float(distance)
                }
            )

    return results


# ==================================================
# IDENTIFY IMPORTANT RESUME SECTIONS
# ==================================================

def get_priority_sections(
    resume_chunks,
    sections
):

    priority_chunks = []

    if not sections:
        return priority_chunks


    # Sections that are particularly important
    # for job-fit questions.

    priority_names = [
        "projects",
        "internships",
        "technical skills",
        "skills",
        "education"
    ]


    for priority_name in priority_names:

        for section_name, section_text in sections.items():

            if section_name.lower() != priority_name:
                continue

            if not section_text:
                continue

            section_text = section_text.strip()

            if len(section_text) < 20:
                continue


            # ==================================================
            # PROJECTS
            # ==================================================

            if priority_name == "projects":

                project_blocks = re.split(
                    r"\n(?=[A-Z][^\n]{2,80}\|)",
                    section_text
                )

                if len(project_blocks) == 1:

                    project_blocks = re.split(
                        r"\n(?=[A-Z][A-Za-z0-9 ]{2,80}\s+-)",
                        section_text
                    )

                for project in project_blocks:

                    project = project.strip()

                    if len(project) > 30:

                        priority_chunks.append(
                            "Resume Section: Projects\n"
                            + clean_text(project)
                        )


            # ==================================================
            # OTHER PRIORITY SECTIONS
            # ==================================================

            else:

                priority_chunks.append(
                    f"Resume Section: "
                    f"{section_name.title()}\n"
                    f"{clean_text(section_text)}"
                )


    return priority_chunks


# ==================================================
# GENERATE RAG RESPONSE
# ==================================================

def generate_rag_response(
    question,
    resume_text,
    job_description="",
    sections=None
):

    # ==================================================
    # GET HUGGING FACE TOKEN
    # ==================================================

    token = get_hf_token()

    if not token:

        return (
            "Hugging Face token not found.\n\n"
            "Please configure the HF_TOKEN environment "
            "variable before using the AI assistant."
        )


    # ==================================================
    # CREATE RESUME KNOWLEDGE BASE
    # ==================================================

    resume_chunks = create_chunks(
        resume_text,
        sections
    )


    # ==================================================
    # CREATE JOB DESCRIPTION CHUNKS
    # ==================================================

    job_chunks = []

    if job_description.strip():

        job_chunks = create_chunks(
            job_description
        )


    # ==================================================
    # BUILD VECTOR DATABASE
    # ==================================================

    all_chunks = list(
        resume_chunks
    )

    for chunk in job_chunks:

        all_chunks.append(
            "Job Description:\n"
            + chunk
        )


    index, _ = build_vector_index(
        all_chunks
    )


    # ==================================================
    # RETRIEVE SEMANTICALLY RELEVANT INFORMATION
    # ==================================================

    retrieved = retrieve_chunks(
        question,
        all_chunks,
        index,
        top_k=5
    )


    # ==================================================
    # BUILD CONTEXT
    # ==================================================

    context_parts = []


    # --------------------------------------------------
    # 1. ALWAYS INCLUDE IMPORTANT RESUME SECTIONS
    # --------------------------------------------------

    priority_chunks = get_priority_sections(
        resume_chunks,
        sections
    )


    for chunk in priority_chunks:

        if chunk not in context_parts:

            context_parts.append(
                chunk
            )


    # --------------------------------------------------
    # 2. ADD FAISS RETRIEVED INFORMATION
    # --------------------------------------------------

    for item in retrieved:

        chunk = item["text"]

        if chunk not in context_parts:

            context_parts.append(
                chunk
            )


    # --------------------------------------------------
    # 3. ADD JOB DESCRIPTION
    # --------------------------------------------------

    for chunk in job_chunks:

        jd_chunk = (
            "Job Description:\n"
            + chunk
        )

        if jd_chunk not in context_parts:

            context_parts.append(
                jd_chunk
            )


    # ==================================================
    # LIMIT CONTEXT SIZE
    # ==================================================

    # Keep enough information for the LLM while
    # preventing unnecessary repetition.

    context_parts = context_parts[:12]


    context = "\n\n".join(
        context_parts
    )


    if not context:

        return (
            "I could not find enough relevant "
            "information in the provided resume."
        )


    # ==================================================
    # STRICT RAG PROMPT
    # ==================================================

    prompt = f"""
You are an AI Resume Assistant.

Your job is to analyze a candidate's resume against
a job description and answer the user's question.

You MUST follow these rules.

==================================================
FACTUAL ACCURACY
==================================================

1. Use ONLY information explicitly present in the
   provided resume context.

2. NEVER invent or assume:

   - skills
   - programming languages
   - projects
   - internship experience
   - work experience
   - education
   - certifications
   - achievements
   - responsibilities
   - technologies
   - communication skills
   - leadership skills
   - problem-solving skills

3. If something exists in the resume context,
   acknowledge it.

4. NEVER say that projects, internships, education,
   or skills are missing if they are explicitly
   present in the provided resume context.

5. If a job requirement is not present in the resume,
   describe it as:

   "Not explicitly mentioned in the resume."

6. Do not infer a skill just because it is normally
   associated with a project.

7. Clearly distinguish between:

   - Resume Evidence
   - Job Requirement
   - Missing Skill

==================================================
IMPORTANT
==================================================

The resume context contains important sections such as:

Projects
Internships
Technical Skills
Education

Read these sections carefully before deciding
whether the candidate has relevant experience.

==================================================
RESPONSE FORMAT
==================================================

Give a professional and concise answer.

Use clean Markdown.

For a job-fit question, prefer this structure:

# Overall Fit

Brief explanation of the candidate's fit.

## Matching Skills

- Mention skills explicitly present in the resume
  that match the job description.

## Relevant Projects

- Mention relevant projects from the resume.
- Explain briefly why each is relevant.

## Relevant Internship Experience

- Mention relevant internship experience if present.

## Skill Gaps

- Mention only important requirements that are not
  explicitly present in the resume.

## Final Assessment

Give a short overall assessment based only on
the evidence.

Do NOT create unnecessary sections.

Do NOT repeat the entire resume.

Do NOT make unsupported claims.

Do NOT claim the candidate has a skill merely because
the job requires it.

==================================================
RESUME / JOB CONTEXT
==================================================

--------------------

{context}

--------------------

USER QUESTION

{question}

==================================================

FINAL INSTRUCTION

Answer the user's question using ONLY the provided
resume and job-description context.

Be factual.

Use the actual projects and internship when they
are relevant.

If something is not present, clearly say so.

Never present an assumption as a resume fact.
"""


    # ==================================================
    # HUGGING FACE CLIENT
    # ==================================================

    client = InferenceClient(
        api_key=token,
        provider="featherless-ai"
    )


    # ==================================================
    # GENERATE RESPONSE
    # ==================================================

    try:

        response = client.chat.completions.create(

            model=LLM_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are a factual and professional "
                        "AI resume analysis assistant. "
                        "Always use the actual resume evidence "
                        "provided in the context. "
                        "Never invent information."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            max_tokens=700
        )


        return (
            response
            .choices[0]
            .message
            .content
        )


    # ==================================================
    # ERROR HANDLING
    # ==================================================

    except Exception as e:

        return (
            "Unable to generate AI response.\n\n"
            f"Error: {str(e)}"
        )