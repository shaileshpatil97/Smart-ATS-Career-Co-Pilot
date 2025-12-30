from celery import shared_task
from uploads.models import ResumeUpload
from analyzer.engine import analyze_resume
from analyzer.utils import extract_text_from_pdf   # IMPORTANT

@shared_task(bind=True)
def process_resume(self, resume_id):
    resume = ResumeUpload.objects.get(id=resume_id)

    resume.status = "PROCESSING"
    resume.save(update_fields=["status"])

    try:
        # 1. Extract PDF text first
        text = extract_text_from_pdf(resume.resume_file.path)
        resume.extracted_text = text
        resume.save(update_fields=["extracted_text"])

        # 2. Now run NLP engine
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
