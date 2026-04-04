import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text, job_description):

    prompt = f"""
    You are an expert career advisor.

    Analyze the resume against the job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide:
    1. Strengths
    2. Missing Skills
    3. Improvement Suggestions
    4. Final Recommendation (Short)

    Keep it concise and structured.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content