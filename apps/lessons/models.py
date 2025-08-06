# apps/lessons/models.py

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


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
# 教材ノードモデル：教材内の章・節・項など階層構造を持つ要素を表現
# ------------------------------------------------------------------------------
class MaterialNode(models.Model):
    material = models.ForeignKey(Material, related_name='material_nodes', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)         # ノードのタイトル（例：第1章）
    description = models.TextField("説明", blank=True, null=True) # ノードの補足説明
    order = models.PositiveBigIntegerField("表示順", default=0)  # 表示順（昇順で並ぶ）

    def clean(self):
        # 親ノードに自分自身を指定していないかをチェック
        if self.parent and self.pk == self.parent.pk:
            raise ValidationError("親ノードに自分自身を指定することはできません。")

        # 再帰的に親をたどって、自分がどこかで親になっていないかをチェック（循環参照防止）
        parent = self.parent
        while parent:
            if parent.pk == self.pk:
                raise ValidationError("循環参照が検出されました。")
            parent = parent.parent

    class Meta:
        ordering = ['order']  # ノードは order に従って昇順に並ぶ
        constraints = [
            models.UniqueConstraint(fields=['parent', 'order'], name='unique_order_per_parent')
        ]
        verbose_name = '教材学習項目'              # 管理画面での単数形表示
        verbose_name_plural = '教材学習項目一覧'   # 管理画面での複数形表示

    def __str__(self):
        # 管理画面などで表示される文字列表現
        return f"学習項目:{self.title}"


#
# ※レッスンモデル：教材に属する章やステップを表現（最終的には削除すること）
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
