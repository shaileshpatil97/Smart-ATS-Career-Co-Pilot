from celery import shared_task
from uploads.models import ResumeUpload
from analyzer.engine import analyze_resume


@shared_task(bind=True)
def process_resume(self, resume_id):
    resume = ResumeUpload.objects.get(id=resume_id)

    resume.status = "PROCESSING"
    resume.save(update_fields=["status"])

    try:
        result = analyze_resume(resume.extracted_text, resume.job_description)

        resume.ats_score = result["score"]
        resume.missing_keywords = result["missing"]
        resume.ai_suggestions = result["suggestions"]
        resume.status = "COMPLETED"
        resume.save()

    except Exception as e:
        resume.status = "FAILED"
        resume.save()
        raise e
