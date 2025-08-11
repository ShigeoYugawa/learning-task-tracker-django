# apps/lessons/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material  # モデルから教材（Material）とレッスン（Lesson）をインポート
from .forms import MaterialForm, MaterialNodeForm , ProgressForm  # フォームもインポート

# ----------------------------------------
# 教材一覧を表示するビュー（関数ベースビュー）
# ----------------------------------------
# @login_required デコレータでログイン済みユーザーのみアクセス許可
# Materialモデルの全件取得し、教材一覧ページのテンプレートに渡す
@login_required
def material_list_view(request):
    materials = Material.objects.all()  # 教材テーブルの全レコードを取得
    return render(request, 'material_list.html', {
        'materials': materials  # テンプレートで 'materials' 変数として利用可能
    })

# ----------------------------------------
# 教材を新規登録するビュー
# ----------------------------------------
@login_required
def material_create(request):
    if request.method == 'POST':
        # POSTリクエスト（フォーム送信時）の場合、送信データでフォームを初期化
        form = MaterialForm(request.POST)
        if form.is_valid():  # フォームのバリデーションチェック
            material = form.save(commit=False)  # DB保存直前のオブジェクトを作成
            material.user = request.user  # ログインユーザーを紐付ける（所有者として）
            material.save()  # DBに保存
            return redirect('lessons:material_list')  # 教材一覧ページへリダイレクト
    else:
        # GETリクエスト（初回アクセス時など）は空フォームを作成
        form = MaterialForm()
    # フォームをテンプレートに渡して表示
    return render(request, 'material_form.html', {'form': form})


# ----------------------------------------
# 指定教材の学習項目追加ビュー
# ----------------------------------------
@login_required
def material_node_create(request):
    if request.method == 'POST':
        form = MaterialNodeForm(request.POST)
        if form.is_valid():
            material_node = form.save(commit=False)
            # 必要あれば所有者の紐付けなど
            material_node.save()
            return redirect('lessons:material_detail', pk=material_node.material.pk)
    else:
        form = MaterialNodeForm()
    return render(request, 'materialnode_form.html', {'form': form})



# ----------------------------------------
# 指定教材の詳細表示ビュー
# ----------------------------------------
# pkで指定されたMaterialインスタンスを取得（存在しなければ404）
# その教材に紐づくLessonの一覧も取得してテンプレートへ渡す
@login_required
def material_detail_view(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'material_detail.html', {'material': material})


# ----------------------------------------
# ホーム画面表示ビュー
# ----------------------------------------
# 認証済みユーザー専用のホームページとして利用
@login_required
def home(request):
    # 特に追加情報は渡さず、home.htmlテンプレートを表示するだけ
    return render(request, 'home.html')
