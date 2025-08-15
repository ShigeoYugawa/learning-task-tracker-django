# apps/learning_content/urls.py

from django.urls import path
from . import views

app_name = 'learning_content'

urlpatterns = [
    path('', views.home, name='home'),

    # 教材
    path('materials/', views.material_list_view, name='material_list'),
    path('materials/create/', views.material_create, name='material_create'),
    path(
        'materials/<int:pk>/', 
        views.material_detail_view, 
        name='material_detail'
    ),

    # 教材および教材ノードの複製
    path(
        'material/<int:template_id>/duplicate/', 
        views.material_duplicate_view, 
        name='material_duplicate'
    ),

    # 教材ノードの追加
    path(
        '<int:material_id>/nodes/add/', 
        views.material_node_create_view, 
        name='material_node_create'
    ),

    # 教材ノードの編集（複製済編集）
    path(
        'materials/<int:material_id>/edit/', 
        views.material_update, 
        name='material_update'
    ),

    # 複製済教材へ学習項目を追加
    path(
        'materials/<int:material_id>/nodes/add_copy/',
        views.material_node_create_for_copy,
        name='material_node_create_for_copy'
    ),

    # 複製済教材の既存学習項目を編集
    path(
        'material_nodes/<int:pk>/edit_copy/',
        views.material_node_edit_for_copy,
        name='material_node_edit_for_copy'
    ),

    # 進捗
    path(
        'progress/create/<int:material_node_id>/', 
        views.progress_create, 
        name='progress_create'
    ),
]

