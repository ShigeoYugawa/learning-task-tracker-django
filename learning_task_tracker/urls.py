"""
URL configuration for learning_task_tracker project.

このファイルはプロジェクト全体のルーティング設定を定義します。
各アプリケーションのURLconf（urls.py）を include() 関数で取り込むことで構成します。
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 管理サイト（/admin/）
    path('admin/', admin.site.urls),

    # アプリ「core」のURLルーティングをルートURLにマッピング
    path('', include('apps.core.urls')),

    # Djangoのデフォルト認証用URL群（login/logout/password_changeなど）
    path('accounts/', include('django.contrib.auth.urls')),
]
