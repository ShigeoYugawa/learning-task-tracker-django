from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Material, Lesson

class MaterialListView(ListView):
    model = Material
    template_name = 'core/material_list.html'
    context_object_name = 'materials'

class MaterialDetailView(DetailView):
    model = Material
    template_name = 'core/material_detail.html'
    context_object_name = 'material'

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'core/lesson_detail.html'
    context_object_name = 'lesson'

def home(request):
    return render(request, 'core/home.html')
