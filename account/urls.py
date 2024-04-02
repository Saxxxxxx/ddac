from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register', views.sign_up, name='signup'),
    path('accounts/profile', views.view_profile, name='view_profile'),
]