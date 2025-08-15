# apps/accounts/forms.py

from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Role
from django.contrib.auth import authenticate
from django.conf import settings


class CustomUserAdminChangeForm(forms.ModelForm):
    """
    管理画面用のユーザー編集フォーム
    - roles を個別チェックボックスで表示
    """
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserAdminCreationForm(UserCreationForm):
    """
    管理画面用のユーザー作成フォーム
    - roles を個別チェックボックスで表示
    """
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'roles')


class CustomUserCreationForm(UserCreationForm):
    """
    UserCreationForm を拡張したユーザー登録フォーム。
    email を必須フィールドとして追加し、ニックネームとパスワードを入力。
    """

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


    def clean_email(self) -> str:
        """
        emailフィールド専用のバリデーションメソッド

        呼び出されるタイミング：
        - フォームの is_valid() を呼んだとき
        - 自動的に clean_email() が呼ばれ、戻り値が cleaned_data に格納される

        処理内容：
        1. 入力された email を取得
        2. DB に同じ email が既に存在するか確認
        3. 存在する場合は ValidationError を発生させる
        4. 存在しない場合は email を返す（cleaned_data に格納される）
        """

        # フォームに入力された email の値を取得
        email = self.cleaned_data.get('email')
        # 既に同じ email が存在する場合はエラー
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return email


class CustomLoginForm(AuthenticationForm):
    """
    カスタムログインフォーム。メールアドレス・ユーザー名・両方の認証方式に対応。
    フォーム内部ではフィールド名 'username' を使用し、AUTH_METHOD に応じてラベルとプレースホルダを動的に変更。
    """

    def __init__(self, request=None, *args, **kwargs) -> None:
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


    def confirm_login_allowed(self, user) -> None:
        """
        ユーザーのログイン許可を確認するメソッド。

        呼び出されるタイミング：
        - Django の AuthenticationForm などからログイン処理時に呼ばれる

        処理内容：
        1. ユーザーがアクティブかどうかを確認
        2. アクティブでなければ ValidationError を発生させ、ログインを拒否
        3. 問題なければ何も返さず正常終了
        """

        if not user.is_active:
            raise forms.ValidationError(
                "このアカウントは無効です。", 
                code='inactive'
            )


    def clean(self) -> Dict[str, Any]:
        """
        フォーム全体のバリデーション処理をオーバーライド。

        処理内容：
        1. username と password を取得
        2. FlexibleAuthBackend.authenticate() で認証
        3. 認証成功なら self.user_cache にユーザーオブジェクトを保持
        4. 認証失敗なら ValidationError を発生
        5. confirm_login_allowed() でログイン可否チェック
        6. 最終的に cleaned_data を返す
        """

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # 認証処理
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "ログインID または パスワードが正しくありません。"
                )

            # ログイン許可判定（例：is_active）
            self.confirm_login_allowed(self.user_cache)

        # バリデーション済みデータを返す
        return self.cleaned_data
