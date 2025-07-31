# apps/accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q


class FlexibleAuthBackend(ModelBackend):
    """
    柔軟なログイン認証用のカスタム認証バックエンド。

    settings.AUTH_METHOD に応じて、ログインIDとして使用するフィールドを切り替える。
    - 'email'   : メールアドレスでのみログインを許可
    - 'username': ユーザー名でのみログインを許可
    - 'both'    : メールアドレスまたはユーザー名どちらでもログインを許可

    認証処理では、対象ユーザーの照合後にパスワード検証とアクティブ判定も行う。
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username または password が不足している場合は認証失敗
        if username is None or password is None:
            return None

        UserModel = get_user_model()

        # 認証方式を設定から取得。デフォルトは 'email'
        auth_method = getattr(settings, "AUTH_METHOD", "email")

        # 検索クエリの初期化
        query = Q()

        # 認証方式に応じてクエリを構築
        if auth_method == 'email':
            # email で完全一致（大文字小文字を無視）
            query = Q(email__iexact=username)
        elif auth_method == 'username':
            # username で完全一致（大文字小文字を無視）
            query = Q(username__iexact=username)
        elif auth_method == 'both':
            # email または username のどちらか一致
            query = Q(email__iexact=username) | Q(username__iexact=username)
        else:
            # 想定外の認証モードが設定されていた場合は明示的に例外を発生
            raise ValueError(f"無効な認証方式: {auth_method}")

        try:
            # 条件に一致するユーザーを取得（複数一致時は例外を防ぐため unique 制約が必要）
            user = UserModel.objects.get(query)
        except UserModel.DoesNotExist:
            # 一致するユーザーが存在しない場合は認証失敗
            return None

        # パスワードとユーザーの有効性（例：is_active）をチェック
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
