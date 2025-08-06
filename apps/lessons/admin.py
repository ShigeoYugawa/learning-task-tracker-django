# apps/lessons/admin.py

from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Material, Lesson, Progress, MaterialNode

# --- 管理サイト全体のUIテキストをカスタマイズ ---
admin.site.site_title = "学習管理システム 管理"
admin.site.site_header = "学習管理システム 管理サイト"
admin.site.index_title = "ダッシュボード"

# Inline設定
# Material（教材）の編集画面で、関連するLesson（レッスン）を一緒に編集できるようにする
# --------------------------------------------------------------------------
class LessonInline(admin.TabularInline):  # 横並びのシンプルな形式
    model = Lesson
    extra = 1  # 空の入力フォームを1行表示（新規追加用）


# MaterialNodeのInline設定
# --------------------------------------------------------------------------
class MaterialNodeInline(admin.TabularInline):
    model = MaterialNode
    extra = 1
    fields = ('title', 'description', 'parent', 'order')
    show_change_link = True  # 編集ページへのリンクを表示


# Material管理画面カスタマイズ
# --------------------------------------------------------------------------
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 一覧で表示される列
    search_fields = ('title', 'description')  # タイトルや説明で検索可能に
    inlines = [LessonInline, MaterialNodeInline]  # インラインでLessonおよびMaterialNodeを表示・編集


# MaterialNode管理画面カスタマイズ
# --------------------------------------------------------------------------
@admin.register(MaterialNode)
class MaterialNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'parent', 'order')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            # 編集中のMaterialNodeのインスタンスIDをURLなどから取得
            object_id = request.resolver_match.kwargs.get('object_id')
            if object_id:
                try:
                    current_node = MaterialNode.objects.get(pk=object_id)
                    # 同じMaterialのノードだけを親候補にする
                    kwargs["queryset"] = MaterialNode.objects.filter(material=current_node.material)
                except MaterialNode.DoesNotExist:
                    pass
            else:
                # 新規作成時は空のクエリセットにするなど工夫可
                kwargs["queryset"] = MaterialNode.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"保存できません: {e.message}", level='error')


# ※Lesson管理画面カスタマイズ （最終的には削除すること）
# --------------------------------------------------------------------------
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


# Progress管理画面カスタマイズ
# --------------------------------------------------------------------------
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'status', 'date')  # 一覧で表示される列
    search_fields = ('lesson__title',)  # レッスンタイトルで検索可能に
    list_filter = ('status', 'date')  # ステータスや日付で絞り込み
