# apps/lessons/urls.py

from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.home, name='home'),  # トップページ
    path('materials/', views.material_list_view, name='material_list'),
    path('materials/<int:pk>/', views.material_detail_view, name='material_detail'),
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson_detail'),
]
