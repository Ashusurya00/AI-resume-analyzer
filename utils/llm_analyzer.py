"""
Enterprise LLM Analyzer
Returns a rich structured analysis with 9 dimensions as a typed dict.
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from config.settings import settings

load_dotenv()

client = OpenAI(api_key=settings.openai_api_key or os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a world-class executive career coach and ATS expert with 20+ years
of experience placing candidates at FAANG, top startups, and Fortune 500 firms.
You provide honest, specific, data-driven resume evaluations.
Always respond with ONLY valid JSON — no preamble, no markdown fences, no extra text."""

def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyze a resume against a job description.
    Returns a structured dict with 9 evaluation dimensions.
    """
    prompt = f"""Analyze this resume against the job description and return ONLY a JSON object
with exactly this structure (all fields required):

{{
  "fit_level": "Strong Fit | Moderate Fit | Weak Fit",
  "ats_score": <integer 0-100>,
  "overall_impression": "<2-3 sentence executive summary of the candidate>",
  "strengths": [
    "<specific strength 1>",
    "<specific strength 2>",
    "<specific strength 3>",
    "<specific strength 4>"
  ],
  "weaknesses": [
    "<specific gap or weakness 1>",
    "<specific gap or weakness 2>",
    "<specific gap or weakness 3>"
  ],
  "missing_skills": [
    "<critical missing skill/experience 1>",
    "<critical missing skill/experience 2>",
    "<critical missing skill/experience 3>"
  ],
  "improvement_suggestions": [
    "<actionable suggestion 1 — be specific about what to add/change>",
    "<actionable suggestion 2>",
    "<actionable suggestion 3>",
    "<actionable suggestion 4>",
    "<actionable suggestion 5>"
  ],
  "bullet_rewrites": [
    {{
      "original": "<copy an actual bullet from the resume>",
      "improved": "<rewritten version with stronger action verbs, metrics, impact>"
    }},
    {{
      "original": "<another bullet>",
      "improved": "<improved version>"
    }}
  ],
  "final_recommendation": "<1 clear paragraph with a hiring recommendation and next steps>"
}}

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}
"""

    try:
        response = client.chat.completions.create(
            model=settings.model_name,
            temperature=settings.temperature,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)

    except json.JSONDecodeError:
        # Return raw text wrapped in fallback structure
        return _fallback(response.choices[0].message.content)
    except Exception as exc:
        return _fallback(str(exc))


def _fallback(raw_text: str) -> dict:
    return {
        "fit_level": "Analysis Error",
        "ats_score": 0,
        "overall_impression": raw_text[:300],
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "improvement_suggestions": [],
        "bullet_rewrites": [],
        "final_recommendation": raw_text,
    }
