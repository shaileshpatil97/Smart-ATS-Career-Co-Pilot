from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('delete/', views.delete_account, name='delete_account'),

]
