# apps/lessons/urls.py

from django.urls import path
from . import views

app_name = 'lessons' # 名前空間

urlpatterns = [
    path('', views.home, name='home'),  # トップページ
    path('materials/', views.material_list_view, name='material_list'),
    path('materials/<int:pk>/', views.material_detail_view, name='material_detail'),
    path('materials/create/', views.material_create, name='material_create'),
    path('lessons/create/', views.lesson_create_view, name='lesson_create'),
    path('materials/<int:material_pk>/lessons/create/', views.lesson_create_view, name='lesson_create_with_material'),
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson_detail'),
    path('lessons/<int:lesson_pk>/progress/create/', views.progress_create_view, name='progress_create'),
]
