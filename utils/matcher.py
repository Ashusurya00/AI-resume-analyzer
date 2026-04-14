"""
Enterprise Skill Extractor & Matcher
Category-aware extraction, alias resolution, and weighted scoring.
"""

import re
from utils.skills import SKILLS_DB, ALL_SKILLS, SKILL_ALIASES


def _normalize(text: str) -> str:
    return SKILL_ALIASES.get(text.lower().strip(), text.lower().strip())


def extract_skills(text: str) -> dict[str, list[str]]:
    """
    Extract skills from text, organized by category.
    Returns { category: [skill, ...] }
    """
    text_lower = text.lower()
    found: dict[str, list[str]] = {}

    for category, skills in SKILLS_DB.items():
        matches = []
        for skill in skills:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                canonical = _normalize(skill)
                if canonical not in matches:
                    matches.append(canonical)
        if matches:
            found[category] = sorted(matches)

    return found


def flatten_skills(skills_by_category: dict[str, list[str]]) -> list[str]:
    """Flatten category dict to a plain list."""
    return [s for skills in skills_by_category.values() for s in skills]


def calculate_match(
    resume_skills: dict[str, list[str]],
    jd_skills: dict[str, list[str]],
) -> dict:
    """
    Compute an advanced match report between resume and JD skills.

    Returns:
        overall_score   : int 0–100
        category_scores : { category: { matched, missing, score } }
        matched_skills  : list[str]
        missing_skills  : list[str]
        priority_missing: top 10 most important missing skills
    """
    resume_flat = set(flatten_skills(resume_skills))
    jd_flat     = set(flatten_skills(jd_skills))

    if not jd_flat:
        return {
            "overall_score": 0,
            "category_scores": {},
            "matched_skills": [],
            "missing_skills": [],
            "priority_missing": [],
        }

    matched  = sorted(resume_flat & jd_flat)
    missing  = sorted(jd_flat - resume_flat)
    score    = round((len(matched) / len(jd_flat)) * 100)

    # Per-category breakdown
    category_scores: dict[str, dict] = {}
    for cat, jd_cat_skills in jd_skills.items():
        jd_set = set(jd_cat_skills)
        res_set = set(resume_skills.get(cat, []))
        cat_matched = sorted(res_set & jd_set)
        cat_missing = sorted(jd_set - res_set)
        cat_score = round((len(cat_matched) / len(jd_set)) * 100) if jd_set else 100
        category_scores[cat] = {
            "matched": cat_matched,
            "missing": cat_missing,
            "score": cat_score,
            "total": len(jd_set),
        }

    # Priority missing: skills from high-signal categories first
    priority_order = [
        "Programming Languages", "Data & AI", "Backend & Cloud",
        "Web & Frontend", "Databases", "Tools & Practices",
        "Domain & Business", "Soft Skills",
    ]
    priority_missing: list[str] = []
    for cat in priority_order:
        if cat in category_scores:
            priority_missing.extend(category_scores[cat]["missing"])
    # Add any remaining
    for s in missing:
        if s not in priority_missing:
            priority_missing.append(s)

    return {
        "overall_score": score,
        "category_scores": category_scores,
        "matched_skills": matched,
        "missing_skills": missing,
        "priority_missing": priority_missing[:10],
    }
