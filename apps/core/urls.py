# apps/core/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# アプリ「core」のURLルーティング設定
urlpatterns = [
    # ホーム画面（説明やナビゲーション用）
    path('', views.home, name='home'),

    # 教材一覧と詳細（FBVに合わせて修正）
    path('materials/', views.material_list_view, name='material_list'),
    path('materials/<int:pk>/', views.material_detail_view, name='material_detail'),

    # レッスン詳細（教材に属する章など）（FBVに合わせて修正）
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson_detail'),

    # 認証関連：ログインページ（カスタムテンプレートを指定）
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # 認証関連：ログアウト（ログアウト後にログイン画面へリダイレクト）
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]
