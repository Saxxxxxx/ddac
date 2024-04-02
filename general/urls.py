from django.urls import path
from . import views

urlpatterns = [
    path('general/home', views.home, name='home'),
    path('general/about-us', views.about_us, name='about_us'),
]
