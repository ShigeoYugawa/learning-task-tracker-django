from django.db import models

# 教材モデル（例：書籍、講座、チュートリアル）
class Material(models.Model):
    title = models.CharField(max_length=100)  # 教材タイトル
    description = models.TextField(blank=True)  # 教材の説明（任意）

    def __str__(self):
        return self.title

# 教材に含まれる各レッスン（章やステップ）
class Lesson(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="lessons")  # 教材とのリレーション
    title = models.CharField(max_length=100)  # レッスンタイトル
    order = models.IntegerField()  # 表示順序

    class Meta:
        ordering = ['order']  # 表示順をorder順に固定

    def __str__(self):
        return f"{self.material.title} - {self.title}"

# 学習の進捗を記録するモデル
class Progress(models.Model):
    STATUS_CHOICES = [
        ("not_started", "未開始"),
        ("in_progress", "学習中"),
        ("done", "完了"),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progresses")  # 対象レッスン
    date = models.DateField(auto_now_add=True)  # 進捗の記録日（自動）
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # 学習ステータス

    def __str__(self):
        return f"{self.lesson.title} - {self.get_status_display()} ({self.date})"
