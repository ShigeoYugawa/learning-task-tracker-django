# apps/lessons/forms.py

from django import forms
from .models import Material, MaterialNode, Progress  # 各モデルをインポート

# ----------------------------------------
# 教材（Material）用フォーム
# ModelFormを継承し、Materialモデルのtitle, descriptionフィールドをフォームに使用
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material  # 対象モデル
        fields = ['title', 'description']  # フォームに表示・入力するフィールド


# ----------------------------------------
# 教材（Material）用フォーム
class MaterialNodeForm(forms.ModelForm):
    class Meta:
        model = MaterialNode
        fields = ['material', 'parent', 'title', 'description', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # parentフィールドの選択肢を絞り込むなどのカスタマイズも可能（必要に応じて）


# ----------------------------------------
# 進捗（Progress）用フォーム
# Progressモデルのstatusフィールドだけをフォームに使用（例: 進捗状況のステータス）
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['status']
