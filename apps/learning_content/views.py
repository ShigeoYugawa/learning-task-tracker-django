# apps/learning_content/views.py

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Material, MaterialNode
from .forms import MaterialForm, MaterialNodeForm, ProgressForm
from .services import duplicate_material


@login_required
def material_list_view(request) -> HttpResponse:
    """
    教材一覧を表示するビュー（関数ベースビュー）
    共有教材（is_template=True）と、自分が所有者の教材だけ取得
    """

    user = request.user
    materials = Material.objects.filter(
        Q(is_template=True) | Q(owner=user)
    ).distinct()
    return render(
        request, 
        'learning_content/material_list.html', 
        {'materials': materials}
    )


@login_required
def material_create(request)-> HttpResponse:
    """
    教材を新規登録するビュー
    """

    if request.method == 'POST':
        # POSTリクエスト（フォーム送信時）の場合、送信データでフォームを初期化
        form = MaterialForm(request.POST)
        if form.is_valid():  # フォームのバリデーションチェック
            material = form.save(commit=False)  # DB保存直前のオブジェクトを作成
            material.owner = request.user # ログインユーザーを紐付ける（所有者として）
            material.last_updated_by = request.user
            material.save()  # DBに保存
            return redirect('learning_content:material_list')  # 教材一覧ページへリダイレクト
    else:
        # GETリクエスト（初回アクセス時など）は空フォームを作成
        form = MaterialForm()
    # フォームをテンプレートに渡して表示
    return render(
        request, 
        'learning_content/material_form.html', 
        {'form': form}
    )


@login_required
def material_node_create_view(request, material_id):
    """
    指定教材に学習項目を追加するビュー
    共有教材（is_template=True）または自分の所有教材のみ追加可能
    """
    material = get_object_or_404(
        Material,
        pk=material_id,
        # 他人の非共有教材は拒否
        is_template=True
    ) if request.user.is_superuser else get_object_or_404(
        Material,
        pk=material_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = MaterialNodeForm(request.POST, material=material)
        if form.is_valid():
            material_node = form.save(commit=False)
            material_node.material = material
            material_node.save()
            return redirect('learning_content:material_detail', pk=material.id)
    else:
        form = MaterialNodeForm(material=material)

    return render(
        request,
        'learning_content/material_node_form.html',
        {'form': form, 'material': material}
    )


@login_required
def material_node_create_for_copy(request, material_id)-> HttpResponse:
    """
    複製教材への学習項目追加ビュー
    """

    material = get_object_or_404(
        Material,
        id=material_id,
        owner=request.user,   # 複製後はownerがユーザーになる
        is_template=False     # テンプレート教材ではない
    )

    if request.method == 'POST':
        form = MaterialNodeForm(material=material, data=request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            node.material = material
            node.owner = request.user
            node.last_updated_by = request.user
            node.save()
            return redirect('learning_content:material_detail', pk=material.id)
    else:
        form = MaterialNodeForm(material=material)

    return render(request, 'learning_content/material_node_form.html', {
        'form': form,
        'material': material
    })


@login_required
def material_node_edit_for_copy(request, pk)-> HttpResponse:
    """
    複製教材の学習項目編集ビュー
    """
    
    node = get_object_or_404(
        MaterialNode,
        pk=pk,
        owner=request.user,
        material__is_template=False
    )
    material = node.material

    if request.method == 'POST':
        form = MaterialNodeForm(material=material, data=request.POST, instance=node)
        if form.is_valid():
            updated_node = form.save(commit=False)
            updated_node.last_updated_by = request.user
            updated_node.save()
            return redirect('learning_content:material_detail', pk=material.id)
    else:
        form = MaterialNodeForm(material=material, instance=node)

    return render(request, 'learning_content/material_node_form.html', {
        'form': form,
        'material': material,
        'node': node
    })


@login_required
def material_detail_view(request, pk) -> HttpResponse:
    """
    指定された教材の詳細ページを表示するビュー。
    表示できるのは以下のいずれかに該当する教材のみ:
      - 共有教材（is_template=True）
      - ログインユーザーが所有する教材（owner=user）
    さらに、教材に紐づくトップレベルの学習項目（parentがNULLのノード）を取得し、並び順(order)で表示する。
    """

    user = request.user
    material_qs = Material.objects.filter(
        Q(is_template=True) | Q(owner=user)
    )
    material = get_object_or_404(material_qs, pk=pk)
    top_nodes = material.nodes.filter(parent__isnull=True).order_by('order').prefetch_related('children')

    return render(request, "learning_content/material_detail.html", {
        "material": material,
        "top_nodes": top_nodes,
        "user": user,
    })


@login_required
def material_duplicate_view(request, template_id) -> HttpResponse:
    """
    共有テンプレート教材を複製してユーザー専用教材を作成するビュー
    """

    template = get_object_or_404(Material, pk=template_id, is_template=True)
    new_material = duplicate_material(template, request.user)
    return redirect('learning_content:material_detail', pk=new_material.pk)


@login_required
def material_update(request, material_id):
    """
    説明コメントを追加
    """
    material = get_object_or_404(Material, pk=material_id)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('learning_content:material_detail', material_id=material.id)
    else:
        form = MaterialForm(instance=material)

    return render(request, 'learning_content/material_form.html', {'form': form})


@login_required
def progress_create(request, material_node_id)-> HttpResponse:
    """
    進捗登録ビュー
    """

    material_node = get_object_or_404(MaterialNode, pk=material_node_id)

    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.material_node = material_node
            progress.save()
            return redirect(
                'learning_content:material_detail', 
                pk=material_node.material.pk
            )
    else:
        form = ProgressForm()

    return render(request, 'learning_content/progress_form.html', {
        'form': form,
        'material_node': material_node
    })


@login_required
def home(request)-> HttpResponse:
    """
    ホーム画面表示ビュー
    認証済みユーザー専用のホームページとして利用
    """

    # 特に追加情報は渡さず、home.htmlテンプレートを表示するだけ
    return render(request, 'home.html')
