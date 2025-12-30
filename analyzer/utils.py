from pdfminer.high_level import extract_text_to_fp
from io import StringIO


import re
import fitz  # PyMuPDF

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_resume_text(path):
    output = StringIO()
    try:
        with open(path, 'rb') as f:
            extract_text_to_fp(f, output)
        return output.getvalue()
    except Exception as e:
        return ""



def ats_match_score(resume_text, jd_text):
    resume = clean_text(resume_text)
    jd = clean_text(jd_text)

    resume_words = set(resume.split())
    jd_words = set(jd.split())

    if not jd_words:
        return 0, []

    # Important skill terms (hard skills weight more)
    hard_skills = [
        'python','django','flask','fastapi','sql','mysql','postgresql',
        'pandas','numpy','scikit','sklearn','tensorflow','pytorch',
        'machine','learning','deep','nlp','api','rest','docker','aws'
    ]

    matched = jd_words.intersection(resume_words)
    matched_hard = matched.intersection(set(hard_skills))

    base_score = len(matched) / len(jd_words)
    bonus = (len(matched_hard) * 2) / max(len(jd_words),1)

    score = min(round((base_score + bonus) * 100, 2), 95)

    missing = sorted(list(jd_words - resume_words))
    important_missing = [w for w in missing if len(w) > 3][:60]

    return score, important_missing
