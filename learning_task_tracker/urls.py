# learning_task_tracker/urls.py

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
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.lessons.urls')),  # ルートは lessons が担当
]
