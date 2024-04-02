from django.urls import path
from . import views

urlpatterns = [
    path('food/list', views.food_list, name='food_list'),
    path('food/detail/<int:pk>', views.food_detail, name='food_detail'),
]
