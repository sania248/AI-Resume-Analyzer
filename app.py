import re
import streamlit as st

from parser import (
    extract_text,
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
    extract_sections
)

from analyzer import (
    extract_jd_skills,
    compare_skills,
    calculate_resume_score
)

from rag import generate_rag_response


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==================================================
# HELPER - FORMAT RESUME SECTIONS
# ==================================================

def format_resume_section(text):
    """
    Formats extracted PDF resume text for clean
    display inside Streamlit.
    """

    lines = text.splitlines()
    formatted_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # ------------------------------------------
        # Convert PDF bullet characters to Markdown
        # ------------------------------------------

        if line.startswith(("•", "●", "▪", "◦", "‣", "⁃")):

            line = "- " + line[1:].strip()

        # ------------------------------------------
        # Normalize existing bullet points
        # ------------------------------------------

        elif re.match(r"^[*-]\s+", line):

            line = "- " + re.sub(
                r"^[*-]\s+",
                "",
                line
            )

        # ------------------------------------------
        # Format Technologies
        # ------------------------------------------

        if line.lower().startswith("technologies:"):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Technologies:** "
                    f"{parts[1].strip()}"
                )

        # ------------------------------------------
        # Format common labels
        # ------------------------------------------

        elif line.lower().startswith(
            "programming languages:"
        ):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Programming Languages:** "
                    f"{parts[1].strip()}"
                )

        elif line.lower().startswith(
            "data science:"
        ):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Data Science:** "
                    f"{parts[1].strip()}"
                )

        elif line.lower().startswith(
            "machine learning:"
        ):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Machine Learning:** "
                    f"{parts[1].strip()}"
                )

        elif line.lower().startswith(
            "visualization:"
        ):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Visualization:** "
                    f"{parts[1].strip()}"
                )

        elif line.lower().startswith(
            "web technologies:"
        ):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Web Technologies:** "
                    f"{parts[1].strip()}"
                )

        elif line.lower().startswith(
            "tools:"
        ):

            parts = line.split(":", 1)

            if len(parts) == 2:

                line = (
                    f"**Tools:** "
                    f"{parts[1].strip()}"
                )

        # ------------------------------------------
        # Add formatted line
        # ------------------------------------------

        formatted_lines.append(line)

    # ----------------------------------------------
    # Join lines without creating excessive spacing
    # ----------------------------------------------

    return "\n".join(formatted_lines)


# ==================================================
# TITLE
# ==================================================

st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze your resume, compare it with job "
    "descriptions and ask an AI assistant questions "
    "about your profile."
)


# ==================================================
# RESUME UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


# ==================================================
# MAIN APPLICATION
# ==================================================

if uploaded_file:

    # ==================================================
    # PROCESS RESUME
    # ==================================================

    with st.spinner("Analyzing your resume..."):

        text = extract_text(uploaded_file)

        name = extract_name(text)

        email = extract_email(text)

        phone = extract_phone(text)

        skills = extract_skills(text)

        sections = extract_sections(text)

        resume_analysis = calculate_resume_score(
            name,
            email,
            phone,
            skills,
            sections
        )


    # ==================================================
    # RESUME INFORMATION
    # ==================================================

    st.subheader("📋 Resume Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("**Name**")

        st.write(
            name if name else "Not found"
        )

    with col2:

        st.markdown("**Email**")

        st.write(
            email if email else "Not found"
        )

    with col3:

        st.markdown("**Phone**")

        st.write(
            phone if phone else "Not found"
        )


    # ==================================================
    # RESUME SCORE
    # ==================================================

    st.subheader("📊 Resume Score")

    score = resume_analysis["score"]

    st.metric(
        "Overall Resume Score",
        f"{score}/100"
    )

    if score >= 80:

        st.success(
            "Excellent resume structure!"
        )

    elif score >= 60:

        st.info(
            "Good foundation, but there is room "
            "for improvement."
        )

    else:

        st.warning(
            "Your resume needs some improvements."
        )


    # ==================================================
    # DETECTED SKILLS
    # ==================================================

    st.subheader("🛠️ Detected Skills")

    if skills:

        st.write(
            " • ".join(skills)
        )

    else:

        st.info(
            "No skills detected."
        )


    # ==================================================
    # RESUME SECTIONS
    # ==================================================

    st.subheader("📚 Resume Sections")

    for section_name, section_text in sections.items():

        if not section_text:
            continue

        with st.expander(
            f"📌 {section_name.title()}"
        ):

            formatted_text = format_resume_section(
                section_text
            )

            st.markdown(
                formatted_text
            )


    # ==================================================
    # RESUME IMPROVEMENT SUGGESTIONS
    # ==================================================

    st.subheader(
        "💡 Resume Improvement Suggestions"
    )

    feedback = resume_analysis["feedback"]

    if feedback:

        for suggestion in feedback:

            st.markdown(
                f"- {suggestion}"
            )

    else:

        st.success(
            "No major structural issues detected."
        )


    # ==================================================
    # JOB DESCRIPTION MATCHING
    # ==================================================

    st.divider()

    st.header(
        "🎯 Job Description Matching"
    )

    st.write(
        "Paste a job description below to check "
        "how well your resume matches the role."
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Software Engineer "
            "with experience in Python, SQL, MongoDB, "
            "Node.js and Machine Learning..."
        )
    )


    # ==================================================
    # JOB DESCRIPTION ANALYSIS
    # ==================================================

    if job_description.strip():

        required_skills = extract_jd_skills(
            job_description
        )

        comparison = compare_skills(
            skills,
            required_skills
        )


        # ==================================================
        # JOB MATCH SCORE
        # ==================================================

        st.subheader(
            "📈 Job Match Score"
        )

        match_percentage = comparison[
            "match_percentage"
        ]

        st.metric(
            "Resume–Job Match",
            f"{match_percentage}%"
        )


        # ==================================================
        # MATCHING / MISSING SKILLS
        # ==================================================

        col1, col2 = st.columns(2)

        # -----------------------------------------------
        # MATCHING SKILLS
        # -----------------------------------------------

        with col1:

            st.markdown(
                "### ✅ Matching Skills"
            )

            if comparison["matched"]:

                for skill in comparison["matched"]:

                    st.markdown(
                        f"- ✓ **{skill}**"
                    )

            else:

                st.info(
                    "No matching skills detected."
                )


        # -----------------------------------------------
        # MISSING SKILLS
        # -----------------------------------------------

        with col2:

            st.markdown(
                "### ❌ Missing Skills"
            )

            if comparison["missing"]:

                for skill in comparison["missing"]:

                    st.markdown(
                        f"- {skill}"
                    )

            else:

                st.success(
                    "No major skill gaps detected!"
                )


        # ==================================================
        # JOB-SPECIFIC RECOMMENDATIONS
        # ==================================================

        st.subheader(
            "💡 Job-Specific Recommendations"
        )

        if comparison["missing"]:

            for skill in comparison["missing"]:

                st.markdown(
                    f"- Consider developing **{skill}**"
                )

        else:

            st.success(
                "Your detected skills align well "
                "with this job."
            )


        # ==================================================
        # AI RESUME ASSISTANT
        # ==================================================

        st.divider()

        st.header(
            "🤖 AI Resume Assistant"
        )

        st.write(
            "Ask questions about your resume and "
            "its relevance to this job."
        )

        question = st.text_area(
            "Ask the AI",
            placeholder=(
                "Example: Why am I a good fit for "
                "this job?"
            ),
            height=120
        )


        # ==================================================
        # ASK AI BUTTON
        # ==================================================

        if st.button(
            "✨ Ask AI",
            type="primary"
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Retrieving relevant resume "
                    "information and generating answer..."
                ):

                    answer = generate_rag_response(
                        question=question,
                        resume_text=text,
                        job_description=job_description,
                        sections=sections
                    )


                # ==================================================
                # AI RESPONSE
                # ==================================================

                st.subheader(
                    "🤖 AI Response"
                )

                if answer:

                    st.markdown(
                        answer
                    )

                else:

                    st.warning(
                        "The AI did not return a response."
                    )


    # ==================================================
    # RAW EXTRACTED TEXT
    # ==================================================

    st.divider()

    st.subheader(
        "📄 Extracted Resume Text"
    )

    with st.expander(
        "View extracted text"
    ):

        st.text_area(
            "Resume Content",
            text,
            height=500
        )