#apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Role
from .forms import CustomUserAdminChangeForm, CustomUserAdminCreationForm


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Role モデルの管理画面設定
    - 管理画面でロールの一覧表示・編集・検索を可能にする
    - list_display: 一覧画面で表示するカラム
    - search_fields: 管理画面の検索ボックスで検索できるフィールド
    """
    
    # 管理画面の一覧表示で表示するカラム
    list_display = ('name', 'description')
    
    # 検索可能なフィールド（管理画面上部の検索ボックス）
    search_fields = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """
    CustomUser の管理画面設定
    - 標準の UserAdmin を拡張
    - ユーザーに Role を割り当てられるように roles フィールドを追加
    """

    form = CustomUserAdminChangeForm
    add_form = CustomUserAdminCreationForm
    
    # ユーザー編集画面で表示するフィールドセット
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'nickname')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'roles',
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # ユーザー追加画面で表示するフィールドセット
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'roles'),
        }),
    )
    
    # 管理画面のユーザー一覧で表示するカラム
    list_display = ('username', 'email', 'nickname', 'is_staff')
    
    # 検索可能なフィールド
    search_fields = ('username', 'email', 'nickname')
    
    # 一覧表示時の並び順
    ordering = ('username',)
