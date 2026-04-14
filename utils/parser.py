"""
Enterprise Resume Parser
Extracts and cleans text from PDF resumes with multi-library fallback.
"""

import re
import io


def extract_text_from_pdf(file) -> str:
    """
    Extract text from an uploaded PDF file.
    Tries pdfplumber first (best for structured resumes),
    falls back to pypdf if pdfplumber fails.
    Returns cleaned plain text.
    """
    raw = ""

    # ── Attempt 1: pdfplumber ────────────────────────────────────────────────
    try:
        import pdfplumber
        file_bytes = file.read() if hasattr(file, "read") else file
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    raw += text + "\n"
        if raw.strip():
            return _clean(raw)
    except Exception:
        pass

    # ── Attempt 2: pypdf ─────────────────────────────────────────────────────
    try:
        from pypdf import PdfReader
        if hasattr(file, "seek"):
            file.seek(0)
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw += text + "\n"
        if raw.strip():
            return _clean(raw)
    except Exception:
        pass

    return raw.strip()


def _clean(text: str) -> str:
    """Normalize whitespace and remove junk characters."""
    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)
    # Replace 3+ newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    return text.strip()


def extract_sections(text: str) -> dict[str, bool]:
    """
    Detect whether key resume sections are present.
    Returns a dict of section → found (bool).
    """
    sections = {
        "Experience":  r"\b(experience|work history|employment)\b",
        "Education":   r"\b(education|academic|degree|university|college)\b",
        "Skills":      r"\b(skills|technical skills|competencies)\b",
        "Projects":    r"\b(projects|portfolio|side projects)\b",
        "Summary":     r"\b(summary|objective|profile|about me)\b",
        "Certifications": r"\b(certifications?|licenses?|credentials)\b",
        "Achievements": r"\b(achievements?|awards?|honors?|accomplishments?)\b",
    }
    lower = text.lower()
    return {name: bool(re.search(pattern, lower)) for name, pattern in sections.items()}


def estimate_experience_years(text: str) -> int:
    """
    Rough estimate of years of experience from date ranges in the resume.
    """
    import datetime
    current_year = datetime.datetime.now().year
    years_found = re.findall(r"\b(20\d{2}|19\d{2})\b", text)
    if len(years_found) >= 2:
        years = [int(y) for y in years_found]
        span = current_year - min(years)
        return max(0, min(span, 40))
    return 0
