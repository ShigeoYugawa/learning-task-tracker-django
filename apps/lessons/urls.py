# apps/lessons/urls.py

from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    # ルートURL（空文字）で home ビューを呼び出し。トップページとして利用
    path('', views.home, name='home'),

    # 教材一覧ページ。Materialの一覧表示ビュー
    path('materials/', views.material_list_view, name='material_list'),

    # 教材詳細ページ。pkで指定された教材の詳細表示ビュー
    path('materials/<int:pk>/', views.material_detail_view, name='material_detail'),

    # 教材作成ページ。新規教材登録用フォーム表示・送信
    path('materials/create/', views.material_create, name='material_create'),

]
