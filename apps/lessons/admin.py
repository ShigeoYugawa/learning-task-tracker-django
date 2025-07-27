# apps/lessons/admin.py

from django.contrib import admin
from .models import Material, Lesson, Progress

# --- Inline設定 ---
# Material（教材）の編集画面で、関連するLesson（レッスン）を一緒に編集できるようにする
class LessonInline(admin.TabularInline):  # 横並びのシンプルな形式
    model = Lesson
    extra = 1  # 空の入力フォームを1行表示（新規追加用）

# --- Material管理画面カスタマイズ ---
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 一覧で表示される列
    search_fields = ('title', 'description')  # タイトルや説明で検索可能に
    inlines = [LessonInline]  # インラインでLessonを表示・編集

# --- Lesson管理画面カスタマイズ ---
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'order')  # 一覧で表示される列
    list_filter = ('material',)  # 教材（Material）で絞り込みが可能に

    # 編集画面のレイアウトを分かりやすくセクション分け
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'material'),  # 基本フィールドをまとめる
        }),
        ('詳細設定', {
            'fields': ('order',),  # 表示順序は詳細として分離
            'classes': ('collapse',),  # 折りたたみ可能なセクションに
        }),
    )

    readonly_fields = ('order',)  # 表示順を読み取り専用に（誤操作防止）

# --- Progress管理画面カスタマイズ ---
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'status', 'date')  # 一覧で表示される列
    search_fields = ('lesson__title',)  # レッスンタイトルで検索可能に
    list_filter = ('status', 'date')  # ステータスや日付で絞り込み
