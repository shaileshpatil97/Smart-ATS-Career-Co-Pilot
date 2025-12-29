from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ResumeUpload

@login_required
def upload_resume(request):
    if request.method == 'POST':
        ResumeUpload.objects.create(
            user=request.user,
            resume_file=request.FILES['resume'],
            job_description=request.POST['job_description'],
            status='PROCESSING'
        )
        return redirect('dashboard')
    return render(request, 'uploads/upload.html')
