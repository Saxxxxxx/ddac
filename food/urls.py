from django.urls import path
from . import views

urlpatterns = [
    path('food/list', views.food_list, name='food_list'),
    path('food/detail/<int:pk>', views.food_detail, name='food_detail'),
    path('custom_admin/food',views.admin_food,name='admin_food'),
    path('food/get',views.get_categories,name='get_food_category'),
    path('get-food-listing-data/', views.get_listing_data, name='get_food_listing_data'),
]
