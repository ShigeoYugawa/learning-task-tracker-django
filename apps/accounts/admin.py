from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Django の既定の UserAdmin をそのまま使って登録
admin.site.register(CustomUser, UserAdmin)
