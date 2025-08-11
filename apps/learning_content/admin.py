# apps/learning_content/admin.py

import logging

logger = logging.getLogger(__name__)  # ファイルの先頭で追加（推奨）

from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Material, Progress#, MaterialNode

# --- 管理サイト全体のUIテキストをカスタマイズ ---
admin.site.site_title = "学習管理システム 管理"
admin.site.site_header = "学習管理システム 管理サイト"
admin.site.index_title = "ダッシュボード"


# MaterialNodeのInline設定
# --------------------------------------------------------------------------
'''
class MaterialNodeInline(admin.TabularInline):
    model = MaterialNode
    extra = 1
    fields = ('title', 'description', 'parent', 'order')
    show_change_link = True  # 編集ページへのリンクを表示
'''

# Material管理画面カスタマイズ
# --------------------------------------------------------------------------
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 一覧で表示される列
    search_fields = ('title', 'description')  # タイトルや説明で検索可能に
    #inlines = [MaterialNodeInline]  # インラインでMaterialNodeを表示・編集


# MaterialNode管理画面カスタマイズ
# --------------------------------------------------------------------------
'''
@admin.register(MaterialNode)
class MaterialNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'parent', 'order')
    autocomplete_fields = ['parent']
    search_fields = ['title']  # オートコンプリート用に必要

    class Media:
        js = ('js/materialnode_autocomplete.js',)

    def get_search_results(self, request, queryset, search_term):
        
        #オートコンプリートで表示される親ノード候補を動的に制限する。
        #自ノードやその子孫を除外し、同じMaterial内のノードのみに絞る。
        #一覧画面などオートコンプリート以外の呼び出しでは絞り込みをしない。
        

        # autocomplete用のURLかどうか判定（URLパスに'autocomplete'が含まれるかで判別）
        if 'autocomplete' not in request.path:
            # 通常の一覧画面などでは絞り込みせず、スーパークラスの動作をそのまま返す
            return super().get_search_results(request, queryset, search_term)

        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        object_id = request.resolver_match.kwargs.get('object_id')
        material_id = request.GET.get('material_id')

        if object_id:
            try:
                current_node = MaterialNode.objects.get(pk=object_id)
                # 自分自身とその子孫ノードを除外
                exclude_ids = current_node.get_descendant_ids() | {current_node.pk}
                queryset = queryset.filter(material=current_node.material).exclude(pk__in=exclude_ids)
            except MaterialNode.DoesNotExist:
                queryset = queryset.none()
        elif material_id:
            try:
                material_id_int = int(material_id)
                queryset = queryset.filter(material_id=material_id_int)
            except ValueError:
                queryset = queryset.none()
        else:
            # material_idがない場合は空にする（選択できない状態に）
            queryset = queryset.none()

        return queryset, use_distinct


    def save_model(self, request, obj, form, change):
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"保存できません: {e.message}", level='error')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs['widget'].attrs['placeholder'] = '先に教材を選んでください'
            # 新規追加時、GETパラメータmaterialからmaterial_idを取得
            material_id = request.GET.get('material')
            if material_id:
                # オートコンプリートURLにmaterial_idをクエリパラメータとして追加
                url = reverse('admin:learning_content_materialnode_autocomplete')
                params = urlencode({'material_id': material_id})
                kwargs['widget'].attrs['data-autocomplete-url'] = f"{url}?{params}"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
'''

# Progress管理画面カスタマイズ
# --------------------------------------------------------------------------
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    #list_display = ('material_node', 'status', 'date')  # 一覧で表示される列
    #search_fields = ('material_node__title',)  # レッスンタイトルで検索可能に
    list_display = ('status', 'date')
    search_fields = ()
    list_filter = ('status', 'date')  # ステータスや日付で絞り込み
