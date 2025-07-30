# apps/accounts/forms.py

'''
PoCであるため頻繁な設計変更を考慮して、統合したモジュールとしています。
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

#
# ユーザー登録フォーム（メールアドレス必須）
# -------------------------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="メールアドレス",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'メールアドレス'
        })
    )

    username = forms.CharField(
        label="ニックネーム",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ユーザー名'
        })
    )

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワード'
        })
    )

    password2 = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'もう一度入力してください'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return email


#
# ログインフォーム（メールアドレスベースで認証）
# -------------------------------------------------------------------
class CustomLoginForm(AuthenticationForm):
    '''
    username フィールドをメールアドレスとして扱う（Djangoの認証システム互換のためフィールド名は username のまま）
    '''
    username = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'メールアドレス'
        })
    )

    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワード'
        })
    )

    def confirm_login_allowed(self, user):
        # 必要に応じてユーザー状態のチェックなどをここに記述可能（例: is_active）
        if not user.is_active:
            raise forms.ValidationError("このアカウントは無効です。", code='inactive')

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")

            self.user_cache = authenticate(self.request, username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    def __init__(self, request=None, *args, **kwargs):
        # 認証結果を保持する内部キャッシュを事前に初期化
        # 将来親クラスがこの属性を使っても安全にするため、super() の前に記述
        self.user_cache = None

        # 認証時に使用されるリクエスト情報を保存（AuthenticationFormが使用）
        self.request = request

        # Django標準AuthenticationFormの初期処理
        super().__init__(*args, **kwargs)

