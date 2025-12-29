from django.urls import path
from .views import upload_resume
from .views import upload_resume, dashboard 

urlpatterns = [
    path('', upload_resume, name='upload_resume'),
    path('dashboard/', dashboard, name='dashboard'),

]

