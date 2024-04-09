from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register', views.sign_up, name='signup'),
    path('accounts/profile', views.view_profile, name='view_profile'),
    path('login', views.custom_login_page, name='custom_login_page'),
    path('custom_admin/user',views.admin_users,name='admin_users'),
    path('custom_admin/approve_user',views.admin_approve_users,name='admin_approve_users'),
    path('get-user/',views.get_users,name='get_users')
]