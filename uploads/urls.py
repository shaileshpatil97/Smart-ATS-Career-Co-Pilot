from django.urls import path
from .views import upload_resume, dashboard , view_report

urlpatterns = [
    path('', upload_resume, name='upload_resume'),
    path('dashboard/', dashboard, name='dashboard'),
    path('report/<int:pk>/', view_report, name='view_report'),


]

