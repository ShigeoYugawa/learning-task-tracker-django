# apps/core/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material, Lesson

# ----------------------------------------
# 教材一覧を表示するビュー（関数ベースビュー）
# ----------------------------------------
# ログインユーザーのみアクセス可能（@login_required）
# Materialモデルの全データを取得し、テンプレートに渡す
@login_required
def material_list_view(request):
    materials = Material.objects.all()  # 教材一覧を取得（全件）
    return render(request, 'core/material_list.html', {
        'materials': materials  # テンプレート側で materials 変数として利用可能
    })

# ----------------------------------------
# 教材の詳細を表示するビュー（関数ベースビュー）
# ----------------------------------------
# 指定されたpkのMaterialインスタンスを取得し、存在しなければ404を返す
# また、その教材に紐づくレッスン（Lesson）一覧も取得して表示する
@login_required
def material_detail_view(request, pk):
    material = get_object_or_404(Material, pk=pk)  # 教材を1件取得（存在しなければ404）
    lessons = material.lesson_set.all()            # 教材に関連付けられたレッスン一覧を取得
    return render(request, 'core/material_detail.html', {
        'material': material,  # 教材オブジェクト
        'lessons': lessons     # 教材に紐づくレッスン一覧
    })

# ----------------------------------------
# レッスンの詳細を表示するビュー（関数ベースビュー）
# ----------------------------------------
# pkをもとにレッスンを1件取得し、その内容をテンプレートで表示する
@login_required
def lesson_detail_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)  # レッスンを取得（存在しなければ404）
    return render(request, 'core/lesson_detail.html', {
        'lesson': lesson  # テンプレートにレッスンオブジェクトを渡す
    })

# ----------------------------------------
# ホーム画面の表示ビュー（関数ベースビュー）
# ----------------------------------------
# 認証済みユーザー専用のホームページ（ダッシュボードなどに利用可）
@login_required
def home(request):
    return render(request, 'core/home.html')  # 特にコンテキストなしでテンプレートを表示
