# ✅ apps/learning_content/apps.py

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # 翻訳対応可能にする

class LessonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.learning_content'
    verbose_name = _("レッスン管理")  # ← ここが管理画面に表示されるアプリ名になります