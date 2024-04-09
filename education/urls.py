from django.urls import path
from . import views

urlpatterns = [
    path('education/list', views.education_list, name='education_list'),
    path('custom_admin/articles',views.admin_articles,name='admin_articles'),
    path('get-article-data/',views.get_article,name="get_article")
]
