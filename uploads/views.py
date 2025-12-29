from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ResumeUpload
from analyzer.tasks import process_resume

@login_required
def upload_resume(request):
    if request.method == 'POST':
        resume = ResumeUpload.objects.create(
            user=request.user,
            resume_file=request.FILES['resume'],
            job_description=request.POST['job_description'],
            status='PENDING'
        )
        process_resume.delay(resume.id)
        return redirect('dashboard')
    return render(request, 'uploads/upload.html')

@login_required
def dashboard(request):
    records = ResumeUpload.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'uploads/dashboard.html', {'records': records})

