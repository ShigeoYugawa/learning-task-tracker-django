#apps/lessons/admin.py

from django.contrib import admin
from .models import Material, Lesson, Progress

admin.site.register(Material)
admin.site.register(Lesson)
admin.site.register(Progress)
