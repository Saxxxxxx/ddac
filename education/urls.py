from django.urls import path
from . import views

urlpatterns = [
    path('education/list', views.education_list, name='education_list'),
]
