from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class ResumeUpload(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    resume_file = models.FileField(upload_to='resumes/')
    job_description = models.TextField()
    extracted_text = models.TextField(blank=True, null=True)
    ats_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    missing_keywords = models.TextField(null=True, blank=True)
    ai_suggestions = models.TextField(null=True, blank=True)
