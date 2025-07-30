# apps/accounts/login_view.py

from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm  # カスタムログインフォームをインポート

# Djangoの組み込みLoginViewを継承して、カスタマイズ用のログインビューを作成
class CustomLoginView(LoginView):
    # 使用するフォームクラスを標準からカスタムに置き換え
    authentication_form = CustomLoginForm

    # 使用するテンプレートファイル（HTML）のパスを指定
    template_name = 'accounts/login.html'
