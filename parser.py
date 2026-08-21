import re
import pdfplumber


# --------------------------------------------------
# EXTRACT TEXT FROM PDF
# --------------------------------------------------

def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text(
                x_tolerance=2,
                y_tolerance=3
            )

            if page_text:
                text += page_text + "\n"

    # Normalize spaces while preserving line breaks
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# --------------------------------------------------
# EXTRACT NAME
# --------------------------------------------------

def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    first_line = lines[0]

    if (
        "@" not in first_line
        and not re.search(r"\d{7,}", first_line)
        and len(first_line.split()) <= 6
    ):
        return first_line

    return None


# --------------------------------------------------
# EXTRACT EMAIL
# --------------------------------------------------

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group(0)

    return None


# --------------------------------------------------
# EXTRACT PHONE
# --------------------------------------------------

def extract_phone(text):

    matches = re.findall(
        r"(?<!\d)[6-9]\d{9}(?!\d)",
        text
    )

    if matches:
        return matches[0]

    return None


# --------------------------------------------------
# EXTRACT SKILLS
# --------------------------------------------------

def extract_skills(text):

    skill_list = [

        "Python",
        "Java",
        "C",
        "C++",
        "SQL",

        "MongoDB",
        "MySQL",
        "PostgreSQL",

        "HTML",
        "CSS",
        "JavaScript",
        "React",

        "Node.js",
        "Express.js",

        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",

        "Scikit-learn",
        "Pandas",
        "NumPy",

        "Tableau",
        "Power BI",
        "Matplotlib",

        "Git",
        "GitHub",

        "REST API",
        "REST APIs",

        "Data Structures",
        "Algorithms",
        "DBMS",

        "Flask",
        "Django",
        "Spring Boot"
    ]

    found_skills = []

    lower_text = text.lower()

    for skill in skill_list:

        if skill.lower() in lower_text:

            found_skills.append(skill)

    return found_skills


# --------------------------------------------------
# NORMALIZE RESUME HEADINGS
# --------------------------------------------------

def normalize_heading(line):

    line = line.strip()

    # Remove bullet / numbering characters
    line = re.sub(
        r"^[•●▪◦‣⁃\-\*\d\.\)\s]+",
        "",
        line
    )

    # Normalize spaces
    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip().upper()


# --------------------------------------------------
# CLEAN SECTION CONTENT
# --------------------------------------------------

def clean_section_line(line):

    line = line.strip()

    if not line:
        return ""

    # Convert PDF bullet characters into Markdown bullets
    if re.match(
        r"^[•●▪◦‣⁃]\s*",
        line
    ):

        line = re.sub(
            r"^[•●▪◦‣⁃]\s*",
            "",
            line
        )

        return "- " + line.strip()

    # Convert lines beginning with * or - into bullets
    if re.match(
        r"^[\*\-]\s+",
        line
    ):

        line = re.sub(
            r"^[\*\-]\s+",
            "",
            line
        )

        return "- " + line.strip()

    return line


# --------------------------------------------------
# EXTRACT RESUME SECTIONS
# --------------------------------------------------

def extract_sections(text):

    section_names = [

        "objective",
        "summary",
        "profile",

        "education",

        "projects",

        "experience",
        "work experience",
        "internships",

        "technical skills",
        "skills",

        "certifications",

        "achievements/activities",
        "achievements and activities",
        "achievements",
        "activities",

        "positions of responsibility",

        "extra curricular activities",
        "extracurricular activities",

        "languages",
        "interests"
    ]


    # --------------------------------------------------
    # HEADING MAP
    # --------------------------------------------------

    heading_map = {}

    for section in section_names:

        heading_map[
            section.upper()
        ] = section


    # --------------------------------------------------
    # PROCESS LINES
    # --------------------------------------------------

    lines = text.splitlines()

    sections = {}

    current_section = None

    current_content = []


    # --------------------------------------------------
    # SAVE CURRENT SECTION
    # --------------------------------------------------

    def save_current_section():

        nonlocal current_section
        nonlocal current_content

        if current_section:

            cleaned_content = []

            for item in current_content:

                item = item.strip()

                if item:
                    cleaned_content.append(item)

            content = "\n\n".join(
                cleaned_content
            ).strip()

            if content:

                sections[
                    current_section
                ] = content

        current_content = []


    # --------------------------------------------------
    # READ EACH LINE
    # --------------------------------------------------

    for line in lines:

        cleaned = line.strip()

        if not cleaned:
            continue


        normalized = normalize_heading(
            cleaned
        )


        # --------------------------------------------------
        # CHECK SECTION HEADING
        # --------------------------------------------------

        if normalized in heading_map:

            save_current_section()

            current_section = heading_map[
                normalized
            ]

            continue


        # --------------------------------------------------
        # ADD CONTENT
        # --------------------------------------------------

        if current_section:

            cleaned_content = clean_section_line(
                cleaned
            )

            if cleaned_content:

                current_content.append(
                    cleaned_content
                )


    # --------------------------------------------------
    # SAVE FINAL SECTION
    # --------------------------------------------------

    save_current_section()


    return sections