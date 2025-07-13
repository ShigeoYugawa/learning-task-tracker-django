from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
