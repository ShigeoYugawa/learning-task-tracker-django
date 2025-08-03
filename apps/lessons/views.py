# apps/lessons/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material, Lesson#, Progress
from .forms import MaterialForm, LessonForm, ProgressForm

# ----------------------------------------
# 教材一覧を表示するビュー（関数ベースビュー）
# ----------------------------------------
# ログインユーザーのみアクセス可能（@login_required）
# Materialモデルの全データを取得し、テンプレートに渡す
@login_required
def material_list_view(request):
    materials = Material.objects.all()  # 教材一覧を取得（全件）
    return render(request, 'material_list.html', {
        'materials': materials  # テンプレート側で materials 変数として利用可能
    })

# ----------------------------------------
# 教材を登録するビュー（関数ベースビュー）
# ----------------------------------------
@login_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user  # ログインユーザーに紐づける
            material.save()
            return redirect('lessons:material_list')  # 適宜変更
    else:
        form = MaterialForm()
    return render(request, 'material_form.html', {'form': form})


# ----------------------------------------
# 教材の詳細を表示するビュー（関数ベースビュー）
# ----------------------------------------
# 指定されたpkのMaterialインスタンスを取得し、存在しなければ404を返す
# また、その教材に紐づくレッスン（Lesson）一覧も取得して表示する
@login_required
def material_detail_view(request, pk):
    material = get_object_or_404(Material, pk=pk)  # 教材を1件取得（存在しなければ404）
    lessons = material.lessons.all()            # 教材に関連付けられたレッスン一覧を取得
    return render(request, 'material_detail.html', {
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
    return render(request, 'lesson_detail.html', {
        'lesson': lesson  # テンプレートにレッスンオブジェクトを渡す
    })

@login_required
def lesson_create_view(request, material_pk=None):
    # material_pk が指定されているなら初期設定する
    initial_data = {}
    if material_pk:
        material = get_object_or_404(Material, pk=material_pk)
        initial_data['material'] = material
    else:
        material = None

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            return redirect('lessons:material_detail', pk=lesson.material.pk)
    else:
        form = LessonForm(initial=initial_data)

    return render(request, 'lesson_form.html', {
        'form': form,
        'material': material,  # テンプレートの見出しに使う（任意）
    })


@login_required
def progress_create_view(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.lesson = lesson
            progress.save()
            return redirect('lessons:lesson_detail', pk=lesson.pk)
    else:
        form = ProgressForm()

    return render(request, 'progress_form.html', {
        'form': form,
        'lesson': lesson,
    })



# ----------------------------------------
# ホーム画面の表示ビュー（関数ベースビュー）
# ----------------------------------------
# 認証済みユーザー専用のホームページ（ダッシュボードなどに利用可）
@login_required
def home(request):
    return render(request, 'home.html')  # 特にコンテキストなしでテンプレートを表示
