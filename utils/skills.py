import re

# Basic skill list (we will upgrade later)
SKILLS = [
    "python", "sql", "machine learning", "deep learning",
    "data analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "power bi", "tableau",
    "nlp", "statistics", "excel", "data visualization"
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.add(skill)

    return list(found_skills)