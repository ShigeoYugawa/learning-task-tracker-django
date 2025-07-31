# apps/accounts/forms.py

'''
PoCであるため頻繁な設計変更を考慮して、統合したモジュールとしています。
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

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
    """
    AUTH_METHOD（email / username / both）に応じて
    ログイン画面の username フィールドのラベルやプレースホルダを切り替える。
    Djangoの認証システム互換のため、フォーム内部のフィールド名は必ず 'username' のまま使用する。
    """

    def __init__(self, request=None, *args, **kwargs):
        # 認証時に使用するリクエストオブジェクトを保持
        self.request = request
        # 認証結果を格納する内部キャッシュを初期化
        self.user_cache = None

        # 親クラスの初期化（フィールド定義などをセットアップ）
        super().__init__(*args, **kwargs)

        # settings.py の AUTH_METHOD の値を取得（未設定なら 'email' をデフォルトとする）
        auth_method = getattr(settings, 'AUTH_METHOD', 'email')

        # AUTH_METHODに応じてusernameフィールドのラベルとプレースホルダを動的に変更
        if auth_method == 'email':
            # メールアドレス認証の場合
            label = 'メールアドレス'
            placeholder = 'メールアドレス'
            self.fields['username'] = forms.EmailField(
                label=label,
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': placeholder,
                })
            )
        elif auth_method == 'username':
            # ユーザー名認証の場合
            label = 'ユーザー名'
            placeholder = 'ユーザー名'
            self.fields['username'] = forms.CharField(
                label=label,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': placeholder,
                })
            )
        elif auth_method == 'both':
            # メールアドレスまたはユーザー名の両方を認証可能にする場合
            label = 'メールアドレス または ユーザー名'
            placeholder = 'メールアドレス または ユーザー名'
            self.fields['username'] = forms.CharField(
                label=label,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': placeholder,
                })
            )

        # password フィールドのUI設定（クラスとプレースホルダ）を更新
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード'
        })

    def confirm_login_allowed(self, user):
        """
        ログイン許可の判定を行うメソッド。
        ここではユーザーがアクティブ状態かどうかをチェックし、
        非アクティブならログインを拒否する。
        """
        if not user.is_active:
            raise forms.ValidationError("このアカウントは無効です。", code='inactive')

    def clean(self):
        """
        フォームのバリデーション処理をオーバーライド。
        入力された username と password を基に認証処理を実施する。

        認証は backends.py の FlexibleAuthBackend.authenticate() に委任し、
        認証成功すれば user_cache にユーザーオブジェクトを保持する。

        失敗した場合は汎用エラーメッセージを返す。
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # settings.AUTH_METHODに応じた認証ロジックを持つ
            # FlexibleAuthBackend による authenticate を呼び出す
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                # 認証失敗時のエラー
                raise forms.ValidationError("ログインID または パスワードが正しくありません。")

            # ログイン許可判定（例：is_active）
            self.confirm_login_allowed(self.user_cache)

        # 最終的にバリデーション済みの cleaned_data を返す
        return self.cleaned_data
