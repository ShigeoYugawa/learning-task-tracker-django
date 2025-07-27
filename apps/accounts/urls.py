# apps/accounts/urls.py

from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .signup_view import user_signup_view

urlpatterns = [
    # ログインビュー（Django標準のLoginViewを使用、テンプレートだけ上書き）
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # ログアウトビュー（ログアウト後は login ページへリダイレクト）
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    # サインアップ（ユーザー登録）ビュー
    path('signup/', user_signup_view, name='signup'),
]
