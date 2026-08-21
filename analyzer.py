import re


# --------------------------------------------------
# SKILL EXTRACTION FROM JOB DESCRIPTION
# --------------------------------------------------

def extract_jd_skills(job_description):
    """
    Extract skills from a job description using skills.txt.
    """

    try:
        with open("skills.txt", "r", encoding="utf-8") as file:
            skills = [
                line.strip()
                for line in file
                if line.strip()
            ]

    except FileNotFoundError:
        return []

    found_skills = []

    jd_text = job_description.lower()

    for skill in skills:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, jd_text):
            found_skills.append(skill)

    return found_skills


# --------------------------------------------------
# SKILL MATCHING
# --------------------------------------------------

def compare_skills(resume_skills, required_skills):
    """
    Compare resume skills with job-required skills.
    """

    # Normalize resume skills
    resume_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    # Remove duplicate required skills
    unique_required = []

    seen = set()

    for skill in required_skills:

        normalized = skill.strip().lower()

        if normalized not in seen:

            seen.add(normalized)
            unique_required.append(skill)


    matched = []
    missing = []


    # Compare skills
    for skill in unique_required:

        if skill.strip().lower() in resume_set:

            matched.append(skill)

        else:

            missing.append(skill)


    # Calculate percentage
    if unique_required:

        match_percentage = (
            len(matched) / len(unique_required)
        ) * 100

    else:

        match_percentage = 0


    return {
        "matched": matched,
        "missing": missing,
        "match_percentage": round(
            match_percentage,
            2
        )
    }


# --------------------------------------------------
# HELPER - CHECK RESUME SECTION
# --------------------------------------------------

def has_section(sections, *section_names):
    """
    Returns True if at least one of the given
    resume sections exists and contains content.
    """

    for section_name in section_names:

        content = sections.get(section_name)

        if content and content.strip():

            return True

    return False


# --------------------------------------------------
# RESUME QUALITY SCORE
# --------------------------------------------------

def calculate_resume_score(
    name,
    email,
    phone,
    skills,
    sections
):
    """
    Calculates a structured resume quality score.
    """

    score = 0
    feedback = []


    # --------------------------------------------------
    # CONTACT INFORMATION - 30 POINTS
    # --------------------------------------------------

    if name:

        score += 10

    else:

        feedback.append(
            "Add your full name."
        )


    if email:

        score += 10

    else:

        feedback.append(
            "Add a professional email address."
        )


    if phone:

        score += 10

    else:

        feedback.append(
            "Add a phone number."
        )


    # --------------------------------------------------
    # TECHNICAL SKILLS - 15 POINTS
    # --------------------------------------------------

    skill_count = len(skills)

    if skill_count >= 10:

        score += 15

    elif skill_count >= 5:

        score += 12

    elif skill_count >= 3:

        score += 8

        feedback.append(
            "Consider adding more relevant technical skills."
        )

    elif skill_count > 0:

        score += 5

        feedback.append(
            "Your resume contains very few detected skills."
        )

    else:

        feedback.append(
            "Add a dedicated technical skills section."
        )


    # --------------------------------------------------
    # OBJECTIVE / SUMMARY - 10 POINTS
    # --------------------------------------------------

    if has_section(
        sections,
        "objective",
        "summary",
        "profile"
    ):

        score += 10

    else:

        feedback.append(
            "Consider adding a concise professional summary."
        )


    # --------------------------------------------------
    # EDUCATION - 10 POINTS
    # --------------------------------------------------

    if has_section(
        sections,
        "education"
    ):

        score += 10

    else:

        feedback.append(
            "Add your education details."
        )


    # --------------------------------------------------
    # PROJECTS - 15 POINTS
    # --------------------------------------------------

    if has_section(
        sections,
        "projects"
    ):

        score += 15

    else:

        feedback.append(
            "Add relevant projects with clear descriptions "
            "and technologies used."
        )


    # --------------------------------------------------
    # EXPERIENCE / INTERNSHIPS - 10 POINTS
    # --------------------------------------------------

    has_experience = has_section(
        sections,
        "experience",
        "work experience",
        "internships"
    )

    if has_experience:

        score += 10

    else:

        feedback.append(
            "Consider adding internships or work experience "
            "if applicable."
        )


    # --------------------------------------------------
    # ACHIEVEMENTS / ACTIVITIES - 5 POINTS
    # --------------------------------------------------

    has_achievements = has_section(
        sections,
        "achievements",
        "achievements/activities",
        "achievements and activities",
        "activities",
        "positions of responsibility",
        "extra curricular activities",
        "extracurricular activities"
    )

    if has_achievements:

        score += 5


    # --------------------------------------------------
    # CERTIFICATIONS
    # --------------------------------------------------

    if not has_section(
        sections,
        "certifications"
    ):

        feedback.append(
            "Consider adding relevant certifications "
            "if you have completed any."
        )


    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    score = min(
        score,
        100
    )


    return {
        "score": score,
        "feedback": feedback
    }


# --------------------------------------------------
# RESUME SUMMARY
# --------------------------------------------------

def generate_resume_summary(
    name,
    skills,
    sections
):
    """
    Generates a structured summary of the resume.
    """

    return {

        "candidate": (
            name
            if name
            else "Candidate"
        ),

        "skill_count": len(
            skills
        ),

        "project_available": has_section(
            sections,
            "projects"
        ),

        "experience_available": has_section(
            sections,
            "experience",
            "work experience",
            "internships"
        ),

        "internship_available": has_section(
            sections,
            "internships"
        ),

        "education_available": has_section(
            sections,
            "education"
        ),

        "achievements_available": has_section(
            sections,
            "achievements",
            "achievements/activities",
            "achievements and activities",
            "activities"
        ),

        "certifications_available": has_section(
            sections,
            "certifications"
        )
    }