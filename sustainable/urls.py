from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from . import views

urlpatterns = [
    path('sustainable/list', views.sustainable_list, name='sustainable_list'),
    path('sustainable/detail/<int:pk>', views.sustainable_detail, name='sustainable_list'),
    path('custom_admin/sustainable',views.admin_sustainable,name='admin_sustainable'),
    path('sustainable/category',views.get_categories,name='get_sustainable_category'),
    path('sustainable/get',views.get_categories,name='get_sustainable_category'),
    path('get-sustainable-listing-data/', views.get_listing_data, name='get_sustainable_listing_data'),
    
]
