import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def rewrite_resume(resume_text, jd_text, missing_keywords):
    prompt = f"""
You are an ATS optimization expert.

Resume:
{resume_text[:4000]}

Job Description:
{jd_text[:2000]}

Missing Keywords:
{missing_keywords}

Rewrite the resume bullet points so that it matches the job description,
naturally inserting missing keywords and improving impact.
Return ONLY improved bullet points.
"""
    return model.generate_content(prompt).text
