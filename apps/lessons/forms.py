# apps/lessons/forms.py

from django import forms
from .models import Material, Lesson, Progress

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'description']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['material', 'title', 'order'] 


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['status']