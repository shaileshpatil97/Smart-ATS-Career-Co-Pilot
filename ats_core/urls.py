from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.shortcuts import redirect ,render

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('upload/', include('uploads.urls')),
    path('accounts/', include('accounts.urls')),   # your signup/login
    path('accounts/', include('django.contrib.auth.urls')),  # Django login/logout
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
