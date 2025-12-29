from celery import shared_task
from uploads.models import ResumeUpload
from .gemini import rewrite_resume

@shared_task
def run_ai_optimizer(resume_id):
    obj = ResumeUpload.objects.get(id=resume_id)
    ai_text = rewrite_resume(obj.extracted_text, obj.job_description, obj.missing_keywords)
    obj.ai_suggestions = ai_text
    obj.save()
