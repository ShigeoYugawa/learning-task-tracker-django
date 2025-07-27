# apps/accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm  # ユーザー作成用の標準フォーム
from django.contrib.auth.models import User  # 標準のUserモデル

# ユーザー登録フォームをカスタマイズしたクラス
class CustomUserCreationForm(UserCreationForm):
    # メールアドレスの入力フィールドを追加（必須項目に設定）
    email = forms.EmailField(required=True)

    class Meta:
        # 使用するモデルとしてDjango標準のUserモデルを指定
        model = User

        # フォームで表示・受け付けるフィールドを定義
        # password1, password2 は UserCreationForm に定義済（パスワード確認用）
        fields = ('username', 'email', 'password1', 'password2')

