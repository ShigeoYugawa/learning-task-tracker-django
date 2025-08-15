# apps/learning_content/forms.py

from django import forms
from django.db.models import Q
from .models import Material, MaterialNode, Progress


class MaterialForm(forms.ModelForm):
    """
    教材（Material）用フォーム
    ModelFormを継承し、Materialモデルのtitle, descriptionフィールドをフォームに使用
    """
    
    class Meta:
        model = Material
        fields = ['title', 'description']  # フォームに表示・入力するフィールド


class MaterialNodeForm(forms.ModelForm):
    """
    教材ノード（MaterialNode）用フォーム
    """

    class Meta:
        model = MaterialNode
        fields = ['title', 'description', 'parent', 'order']
        labels = {
            'title': '項目名',
            'description': '説明',
            'parent': '上位項目',
            'order': '表示順番号',
        }
        help_texts = {
            'order': '同じ章の中で順番が重複しないように、他の項目と異なる番号を指定してください。',
        }


    def __init__(self, *args, **kwargs) -> None:
        material = kwargs.pop('material', None)
        super().__init__(*args, **kwargs)
        if material:
            self.fields['parent'].queryset = material.nodes.all()



class ProgressForm(forms.ModelForm):
    """
    進捗（Progress）用フォーム
    Progressモデルのstatusフィールドだけをフォームに使用（例: 進捗状況のステータス）
    """

    class Meta:
        model = Progress
        fields = ['status']
