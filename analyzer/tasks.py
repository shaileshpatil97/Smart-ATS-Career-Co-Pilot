import pdfplumber
from celery import shared_task
from uploads.models import ResumeUpload
from analyzer.engine import analyze_resume


def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            text += p.extract_text() or ""
    return text


@shared_task(bind=True)
def process_resume(self, resume_id):

    resume = ResumeUpload.objects.get(id=resume_id)
    resume.status = "PROCESSING"
    resume.save()

    try:
        # extract resume text
        text = extract_text_from_pdf(resume.resume_file.path)
        resume.extracted_text = text

        # REAL NLP ATS
        result = analyze_resume(text, resume.job_description)

        resume.ats_score = result["score"]
        resume.missing_keywords = result["missing"]
        resume.ai_suggestions = result["suggestions"]
        resume.status = "COMPLETED"
        resume.save()

    except Exception as e:
        resume.status = "FAILED"
        resume.save()
        raise e
