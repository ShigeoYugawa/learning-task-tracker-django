# apps/lessons/urls.py

from django.urls import path
from . import views

app_name = 'lessons'  # URL名前空間を設定。テンプレートで {% url 'lessons:home' %} のように使うための識別子

urlpatterns = [
    # ルートURL（空文字）で home ビューを呼び出し。トップページとして利用
    path('', views.home, name='home'),

    # 教材一覧ページ。Materialの一覧表示ビュー
    path('materials/', views.material_list_view, name='material_list'),

    # 教材詳細ページ。pkで指定された教材の詳細表示ビュー
    path('materials/<int:pk>/', views.material_detail_view, name='material_detail'),

    # 教材作成ページ。新規教材登録用フォーム表示・送信
    path('materials/create/', views.material_create, name='material_create'),

    path('materials/<int:material_pk>/lessons/', views.lesson_list_view, name='lesson_list'),

    # レッスン作成ページ（教材指定なし）。新規レッスン登録用フォーム
    path('lessons/create/', views.lesson_create_view, name='lesson_create'),

    # 教材に紐づくレッスン作成ページ。material_pkで教材を指定して初期値設定
    path('materials/<int:material_pk>/lessons/create/', views.lesson_create_view, name='lesson_create_with_material'),

    # レッスン詳細ページ。pkで指定されたレッスン詳細を表示
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson_detail'),

    # レッスンに対する進捗登録ページ。lesson_pkでレッスンを指定して進捗作成フォーム表示
    path('lessons/<int:lesson_pk>/progress/create/', views.progress_create_view, name='progress_create'),
]
