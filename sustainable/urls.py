from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from . import views

urlpatterns = [
    path('sustainable/list', views.sustainable_list, name='sustainable_list'),
    path('sustainable/detail/<int:pk>', views.sustainable_detail, name='sustainable_list'),
]
