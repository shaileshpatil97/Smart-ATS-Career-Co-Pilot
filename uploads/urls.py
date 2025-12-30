from django.urls import path
from .views import upload_resume, dashboard , view_report , guest_upload
from django.views.generic import TemplateView


urlpatterns = [
    path('', upload_resume, name='upload_resume'),
    path('dashboard/', dashboard, name='dashboard'),
    path('report/<int:pk>/', view_report, name='view_report'),
    path('guest/', guest_upload, name='guest_upload'),
    path('guest/thankyou/', TemplateView.as_view(template_name="uploads/guest_done.html"), name="guest_thankyou"),




]

