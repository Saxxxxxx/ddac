from django.urls import path
from . import views

urlpatterns = [
    path('general/home', views.home, name='home'),
    path('general/about-us', views.about_us, name='about_us'),
    path('custom_admin/home',views.admin_home,name='admin_home'),
    path('general/get_country',views.get_country,name='get_countries'),
    path('general/profile',views.profile,name='profile')
]
