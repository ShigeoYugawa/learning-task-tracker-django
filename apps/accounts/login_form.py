# accounts/forms/login_form.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm  # Django標準のログインフォーム

# ログインフォームをカスタマイズするクラス（標準のAuthenticationFormを継承）
class CustomLoginForm(AuthenticationForm):
    # ユーザー名入力欄（emailも許容するUI/UX上のヒント付き）
    username = forms.CharField(
        max_length=254,  # 入力最大文字数
        widget=forms.TextInput(attrs={
            'class': 'form-control',                # Bootstrap対応のクラス
            'placeholder': 'ユーザー名またはメールアドレス'  # プレースホルダー表示
        }),
    )

    # パスワード入力欄（パスワード用の非表示フィールドを使用）
    password = forms.CharField(
        label="Password",  # ラベルは「Password」と表示される（必要なら日本語にも変更可）
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',       # Bootstrap用クラス
            'placeholder': 'パスワード'     # ヒントテキスト
        }),
    )
