from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from .models import ResumeUpload
from analyzer.tasks import process_resume
from django.contrib.auth.models import User


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

@login_required
def view_report(request, pk):
    record = ResumeUpload.objects.get(id=pk, user=request.user)
    return render(request, 'uploads/report.html', {'record': record})



from django.http import JsonResponse

@login_required
def job_description_api(request, pk):
    r = ResumeUpload.objects.get(id=pk, user=request.user)
    return JsonResponse({"jd": r.job_description})



def guest_upload(request):
    if request.method == 'POST':
        guest_user, _ = User.objects.get_or_create(username='guest')

        resume = ResumeUpload.objects.create(
            user=guest_user,
            resume_file=request.FILES['resume'],
            job_description=request.POST['job_description'],
            status='PENDING'
        )

        process_resume.delay(resume.id)

        return redirect('guest_result', resume.id)

    return render(request, 'uploads/guest_upload.html')

def guest_result(request, pk):
    record = ResumeUpload.objects.get(id=pk)
    return render(request, 'uploads/guest_result.html', {'record': record})

def resume_status(request, pk):
    r = get_object_or_404(ResumeUpload, id=pk)
    return JsonResponse({
        "status": r.status,
        "score": r.ats_score or 0
    })