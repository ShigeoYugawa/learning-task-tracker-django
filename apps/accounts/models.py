# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 任意の追加フィールド（必要なければ何も追加しなくてもOK）
    nickname = models.CharField("ニックネーム", max_length=30, blank=True)
    
    def __str__(self):
        return self.username
