from celery import shared_task
from uploads.models import ResumeUpload
from .utils import extract_resume_text, ats_match_score

@shared_task(bind=True)
def process_resume(self, resume_id):
    try:
        obj = ResumeUpload.objects.get(id=resume_id)

        text = extract_resume_text(obj.resume_file.path)
        score, missing = ats_match_score(text, obj.job_description)

        obj.extracted_text = text[:10000]
        obj.missing_keywords = ",".join(missing[:100])
        obj.ats_score = score
        obj.status = 'COMPLETED'
        obj.save()

        # 🔥 Call AI task (NO circular import)
        from analyzer.ai_tasks import run_ai_optimizer
        run_ai_optimizer.delay(obj.id)

    except Exception as e:
        obj.status = 'FAILED'
        obj.save()
        raise self.retry(exc=e, countdown=10, max_retries=3)
