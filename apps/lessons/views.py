# apps/lessons/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material, Lesson  # モデルから教材（Material）とレッスン（Lesson）をインポート
from .forms import MaterialForm, LessonForm, ProgressForm  # フォームもインポート

# ----------------------------------------
# 教材一覧を表示するビュー（関数ベースビュー）
# ----------------------------------------
# @login_required デコレータでログイン済みユーザーのみアクセス許可
# Materialモデルの全件取得し、教材一覧ページのテンプレートに渡す
@login_required
def material_list_view(request):
    materials = Material.objects.all()  # 教材テーブルの全レコードを取得
    return render(request, 'lessons/material_list.html', {
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
    return render(request, 'lessons/material_form.html', {'form': form})

# ----------------------------------------
# 指定教材の詳細表示ビュー
# ----------------------------------------
# pkで指定されたMaterialインスタンスを取得（存在しなければ404）
# その教材に紐づくLessonの一覧も取得してテンプレートへ渡す
@login_required
def material_detail_view(request, pk):
    material = get_object_or_404(Material, pk=pk)  # 教材を1件取得 or 404
    lessons = material.lessons.all()  # 外部キーのrelated_name 'lessons' を使い関連レッスン一覧取得
    return render(request, 'lessons/material_detail.html', {
        'material': material,  # 教材オブジェクト
        'lessons': lessons     # 教材に紐づくレッスン一覧
    })


@login_required
def lesson_list_view(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    lessons = material.lessons.all()  # related_name='lessons' を使って取得
    return render(request, 'lessons/lesson_list.html', {
        'material': material,
        'lessons': lessons
    })



# ----------------------------------------
# 指定レッスンの詳細表示ビュー
# ----------------------------------------
# pkで指定されたLessonを取得しテンプレートに渡す
@login_required
def lesson_detail_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)  # レッスン1件取得 or 404
    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson  # レッスンオブジェクトを渡す
    })

# ----------------------------------------
# レッスン新規作成ビュー
# ----------------------------------------
@login_required
def lesson_create_view(request, material_pk=None):
    # material_pk が指定されていれば、その教材を初期値としてフォームにセットする
    initial_data = {}
    if material_pk:
        material = get_object_or_404(Material, pk=material_pk)  # 教材取得 or 404
        initial_data['material'] = material
    else:
        material = None

    if request.method == 'POST':
        form = LessonForm(request.POST)  # 送信データでフォーム初期化
        if form.is_valid():
            lesson = form.save()  # フォーム内容をDBに保存
            # 保存後、関連教材の詳細ページへリダイレクト
            return redirect('lessons:material_detail', pk=lesson.material.pk)
    else:
        form = LessonForm(initial=initial_data)  # GETの場合は初期値設定

    return render(request, 'lessons/lesson_form.html', {
        'form': form,
        'material': material,  # テンプレートで見出しや説明用に利用（任意）
    })

# ----------------------------------------
# 進捗（Progress）作成ビュー
# ----------------------------------------
@login_required
def progress_create_view(request, lesson_pk):
    # 進捗は特定のレッスンに紐づくためlesson_pkを受け取る
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)  # DB保存前にuserとlessonをセット
            progress.user = request.user  # ログインユーザーに紐付け
            progress.lesson = lesson       # 対象のレッスンに紐付け
            progress.save()  # 保存
            return redirect('lessons:lesson_detail', pk=lesson.pk)  # レッスン詳細へ戻る
    else:
        form = ProgressForm()  # GETは空フォーム

    return render(request, 'lessons/progress_form.html', {
        'form': form,
        'lesson': lesson,  # レッスン情報もテンプレートへ渡す
    })

# ----------------------------------------
# ホーム画面表示ビュー
# ----------------------------------------
# 認証済みユーザー専用のホームページとして利用
@login_required
def home(request):
    # 特に追加情報は渡さず、home.htmlテンプレートを表示するだけ
    return render(request, 'home.html')
