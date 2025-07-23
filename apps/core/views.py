#apps/core/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Material, Lesson

# 教材一覧を表示するビュー（クラスベースビュー）
# Materialモデルの全オブジェクトを取得し、テンプレートに渡す
class MaterialListView(ListView):
    model = Material  # 対象のモデル
    template_name = 'core/material_list.html'  # 使用するテンプレート
    context_object_name = 'materials'  # テンプレートで使う変数名

# 教材の詳細を表示するビュー（クラスベースビュー）
# 特定の教材に対して、その詳細情報と関連するレッスンを表示
class MaterialDetailView(DetailView):
    model = Material
    template_name = 'core/material_detail.html'
    context_object_name = 'material'

# レッスンの詳細を表示するビュー（クラスベースビュー）
# 特定のレッスンに関する情報（タイトルや説明など）を表示
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'core/lesson_detail.html'
    context_object_name = 'lesson'

# ログインユーザー向けのホーム画面
# 認証済みユーザーのみがアクセス可能
@login_required
def home(request):
    return render(request, 'core/home.html')
