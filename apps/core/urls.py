from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# アプリ「core」のURLルーティング設定
urlpatterns = [
    # ホーム画面（説明やナビゲーション用）
    path('', views.home, name='home'),

    # 教材一覧と詳細
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),

    # レッスン詳細（教材に属する章など）
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),

    # 認証関連：ログインページ（カスタムテンプレートを指定）
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # 認証関連：ログアウト（ログアウト後にログイン画面へリダイレクト）
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]
