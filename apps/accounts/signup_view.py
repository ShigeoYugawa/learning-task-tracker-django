# apps/accounts/signup_view.py

from django.shortcuts import render, redirect
from django.contrib.auth import login  # 認証済みユーザーとしてログインさせる関数
from .forms import CustomUserCreationForm  # カスタムユーザー登録フォームをインポート

# ユーザーの新規登録処理を担当するビュー関数
def user_signup_view(request):
    # ユーザーがフォームを送信（POST）したときの処理
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # POSTデータを使ってフォームを初期化

        # 入力データがバリデーションを通過したかを確認
        if form.is_valid():
            user = form.save()          # データベースにユーザーを保存
            login(request, user)        # 登録直後に自動でログイン処理
            return redirect('learning_content:material_list')  # タスク一覧画面など、次の画面にリダイレクト

    else:
        # 初回アクセスやGETリクエスト時は空のフォームを表示
        form = CustomUserCreationForm()

    # フォームをテンプレートに渡してレンダリング
    return render(request, 'accounts/signup.html', {'form': form})