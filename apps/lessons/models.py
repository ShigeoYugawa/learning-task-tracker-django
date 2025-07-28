# apps/lessons/models.py

from django.conf import settings
from django.db import models

#
# 教材モデル：学習のベースとなる書籍やチュートリアルなどを表現
# ------------------------------------------------------------------------------
class Material(models.Model):
    title = models.CharField("タイトル", max_length=100)  # 教材のタイトル
    description = models.TextField("説明", blank=True)     # 教材の説明（省略可能）

    def __str__(self):
        # 管理画面などでの表示名
        return f"教材: {self.title}"

    class Meta:
        verbose_name = '教材'              # 管理画面での単数形表示
        verbose_name_plural = '教材一覧'   # 管理画面での複数形表示


#
# レッスンモデル：教材に属する章やステップを表現
# ------------------------------------------------------------------------------
class Lesson(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,      # 教材が削除されたら関連レッスンも削除
        related_name="lessons",        # material.lessons で関連レッスンにアクセス可能
        verbose_name="教材"
    )
    title = models.CharField("レッスンタイトル", max_length=100)  # レッスンのタイトル
    order = models.IntegerField("表示順序")                     # 教材内での並び順を指定

    class Meta:
        ordering = ['order']                  # 表示順は order 昇順に固定
        verbose_name = "レッスン"            # 管理画面での単数形表示
        verbose_name_plural = "レッスン一覧" # 管理画面での複数形表示

    def __str__(self):
        # 例: 「Python入門 > レッスン: 条件分岐」
        return f"{self.material.title} > レッスン: {self.title}"

#
# 進捗モデル：ユーザーがどのレッスンをどこまで学習したかを記録
# ------------------------------------------------------------------------------
class Progress(models.Model):
    STATUS_CHOICES = [
        ("not_started", "未開始"),
        ("in_progress", "学習中"),
        ("done", "完了"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,       # ユーザーが削除されたら進捗も削除
        related_name="progresses",      # user.progresses でアクセス可能
        verbose_name="ユーザー",
        null=False
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,       # レッスンが削除されたら進捗も削除
        related_name="progresses",      # lesson.progresses でアクセス可能
        verbose_name="レッスン"
    )
    date = models.DateField("記録日", auto_now_add=True)  # 進捗の記録日（自動設定）
    status = models.CharField("学習ステータス", max_length=20, choices=STATUS_CHOICES)  # 学習状況を選択肢から指定

    class Meta:
        verbose_name = "進捗"             # 管理画面での単数形表示
        verbose_name_plural = "進捗一覧"  # 管理画面での複数形表示

    def __str__(self):
        # 例: 「Python入門 > レッスン: 条件分岐 の進捗 - 学習中（2025-07-27）」
        return f"{self.lesson} の進捗 - {self.get_status_display()}（{self.date}）"
