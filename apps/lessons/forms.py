# apps/lessons/forms.py

from django import forms
from .models import Material, Lesson, Progress  # 各モデルをインポート

# ----------------------------------------
# 教材（Material）用フォーム
# ModelFormを継承し、Materialモデルのtitle, descriptionフィールドをフォームに使用
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material  # 対象モデル
        fields = ['title', 'description']  # フォームに表示・入力するフィールド


# ----------------------------------------
# レッスン（Lesson）用フォーム
# Lessonモデルのmaterial(外部キー)、title、orderフィールドをフォームに使用
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['material', 'title', 'order'] 


# ----------------------------------------
# 進捗（Progress）用フォーム
# Progressモデルのstatusフィールドだけをフォームに使用（例: 進捗状況のステータス）
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['status']
