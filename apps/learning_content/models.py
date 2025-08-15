# apps/learning_content/models.py

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Material(models.Model):
    """
    教材モデル：学習のベースとなる書籍やチュートリアルなどを表現
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    # 所有者（None の場合は公式・共有ライブラリ教材）
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="materials"
    ) 

    # True の場合は全ユーザー共有のテンプレート教材
    is_template = models.BooleanField(default=False)

    # 「どの公式テンプレートからこの教材が複製されたか」を追跡する
    parent_template = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='derived_materials',
        verbose_name='元テンプレート'
    )

    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,  # ユーザー削除時はNULL
        related_name="updated_materials",
        verbose_name="最終更新者"
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        ordering = ["title"]
        verbose_name = "教材"              # 管理画面での単数形表示
        verbose_name_plural = "教材一覧"   # 管理画面での複数形表示


    def __str__(self) -> str:
        # 管理画面などでの表示名
        return f"教材: {self.title}"


class MaterialNode(models.Model):
    """
    教材ノードモデル：教材内の章・節・項など階層構造を持つ要素を表現
    """

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="nodes"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    order = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="material_nodes"
    )

    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_material_nodes",
        verbose_name="最終更新者"
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    
    def get_descendant_ids(self) -> set[int]:
        """
        自ノードのすべての子孫ノードのIDを返す（再帰的に取得）。

        Returns:
            set[int]: 子孫ノードのIDの集合
        """

        descendants = set()
        for child in self.children.all():
            descendants.add(child.pk)
            descendants.update(child.get_descendant_ids())
        return descendants


    def clean(self) -> None:
        """
        モデルのバリデーション処理を実行する。

        このメソッドでは以下のチェックを行う：
            1. 自分自身を親ノードに設定していないか
            2. 親ノードと同じ教材に属しているか
            3. 階層構造に循環参照が発生していないか

        Raises:
            ValidationError: 上記条件のいずれかに違反した場合に発生
        """

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
        ordering = ["material", "order"]  # ノードは order に従って昇順に並ぶ
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'order'], 
                name='unique_order_per_parent'
            )
        ]
        verbose_name = "教材学習項目"              # 管理画面での単数形表示
        verbose_name_plural = "教材学習項目一覧"   # 管理画面での複数形表示


    def __str__(self) -> str:
        # 管理画面などで表示される文字列表現
        return f"学習項目:{self.material.title} - {self.title}"


class Progress(models.Model):
    """
    進捗モデル：ユーザーがどのレッスンをどこまで学習したかを記録
    """

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
        verbose_name="教材学習項目",
        null=True,        # ← 一時的にNULLを許可
        blank=True        # ← 管理画面で空欄を許可
    )
    # 進捗の記録日（自動設定）
    date = models.DateField(
        verbose_name="記録日", 
        auto_now_add=True,
        null=True
    )
    # 学習状況を選択肢から指定
    status = models.CharField(
        verbose_name="学習ステータス", 
        max_length=20, 
        choices=STATUS_CHOICES
    )


    class Meta:
        verbose_name = "進捗"             # 管理画面での単数形表示
        verbose_name_plural = "進捗一覧"  # 管理画面での複数形表示


    def __str__(self) -> str:
        return (
            f"{self.material_node} の進捗 - "
            f"{self.get_status_display()}（{self.date}）"
        )

