# apps/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    editor_free, editor_paid", adminなど複数の権限を管理する
    """

    name = models.CharField(verbose_name="ロール名", max_length=50, unique=True)
    description = models.TextField(verbose_name="説明", blank=True)


    class Meta:
        verbose_name = "ロール"
        verbose_name_plural = "ロール一覧"


    def __str__(self) -> str:
        # 管理画面やフォームの表示で日本語化
        role_names_jp = {
            "editor_free": "無料エディター",
            "editor_paid": "有料エディター",
            "admin": "管理者"
        }
        return f"ロール：{role_names_jp.get(self.name, self.name)}"
  
    
class CustomUser(AbstractUser):
    """
    カスタムユーザーモデル（標準Userを継承）
    """

    email = models.EmailField("メールアドレス", unique=True)
    nickname = models.CharField("ニックネーム", max_length=30, blank=True)
    roles = models.ManyToManyField(
        Role, 
        blank=True, 
        related_name="users", 
        verbose_name="権限ロール"
    )


    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー一覧"


    def has_role(self, role_name: str) -> bool:
        """
        ユーザーが指定ロールを持っているか判定
        """
        
        return self.roles.filter(name=role_name).exists()


    def __str__(self) -> str:
        return f"ユーザー：{self.username}"