from django.apps import AppConfig

# アプリ「core」の構成設定クラス
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # デフォルトの主キー型
    name = 'apps.core'  # アプリのパス（プロジェクト内での識別用）
