from django.shortcuts import render

# Create your views here.
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
