# apps/lessons/models.py

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


#
# 教材モデル：学習のベースとなる書籍やチュートリアルなどを表現
# ------------------------------------------------------------------------------
class Material(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=100)  # 教材のタイトル
    description = models.TextField(verbose_name="説明", blank=True)     # 教材の説明（省略可能）

    def __str__(self):
        # 管理画面などでの表示名
        return f"教材: {self.title}"

    class Meta:
        verbose_name = "教材"              # 管理画面での単数形表示
        verbose_name_plural = "教材一覧"   # 管理画面での複数形表示


#
# 教材ノードモデル：教材内の章・節・項など階層構造を持つ要素を表現
# ------------------------------------------------------------------------------
class MaterialNode(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_nodes')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    title = models.CharField(verbose_name="タイトル", max_length=200)         # ノードのタイトル（例：第1章）
    description = models.TextField(verbose_name="説明", blank=True, null=True) # ノードの補足説明
    order = models.PositiveBigIntegerField(verbose_name="表示順", default=0)  # 表示順（昇順で並ぶ）

    def get_descendant_ids(self):
        """
        自ノードのすべての子孫ノードのIDを返す（再帰的）。
        """
        descendants = set()
        for child in self.children.all():
            descendants.add(child.pk)
            descendants.update(child.get_descendant_ids())
        return descendants

    def clean(self):
        # 自分自身を親に指定していないか（新規作成時は pk=None なので注意）
        if self.parent and self.pk and self.parent.pk == self.pk:
            raise ValidationError("親ノードに自分自身を指定することはできません。")

        # 同じ教材内かどうかをチェック（任意）
        if self.parent and self.material != self.parent.material:
            raise ValidationError("親ノードは同じ教材内のノードを選択してください。")

        # 循環参照のチェック
        parent = self.parent
        visited = set()
        while parent:
            if self.pk and parent.pk == self.pk:
                raise ValidationError("循環参照が検出されました。")
            if parent.pk in visited:
                break  # 無限ループ防止
            visited.add(parent.pk)
            parent = parent.parent

    class Meta:
        ordering = ['order']  # ノードは order に従って昇順に並ぶ
        constraints = [
            models.UniqueConstraint(fields=['parent', 'order'], name='unique_order_per_parent')
        ]
        verbose_name = "教材学習項目"              # 管理画面での単数形表示
        verbose_name_plural = "教材学習項目一覧"   # 管理画面での複数形表示

    def __str__(self):
        # 管理画面などで表示される文字列表現
        return f"学習項目:{self.title}"


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
    material_node = models.ForeignKey(
        MaterialNode,
        on_delete=models.CASCADE,
        related_name="progresses",
        verbose_name="教材学習項目"
    )
    date = models.DateField(verbose_name="記録日", auto_now_add=True)  # 進捗の記録日（自動設定）
    status = models.CharField(verbose_name="学習ステータス", max_length=20, choices=STATUS_CHOICES)  # 学習状況を選択肢から指定

    class Meta:
        verbose_name = "進捗"             # 管理画面での単数形表示
        verbose_name_plural = "進捗一覧"  # 管理画面での複数形表示

    def __str__(self):
        return f"{self.material_node} の進捗 - {self.get_status_display()}（{self.date}）"

