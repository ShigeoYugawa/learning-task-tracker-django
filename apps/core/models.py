from django.db import models

# 教材（例：書籍やチュートリアル）
class Material(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# 各教材内の章やセクション、順序あり
class Lesson(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.material.title} - {self.title}"

# 学習の進捗状況（ステータス + 日付）
class Progress(models.Model):
    STATUS_CHOICES = [
        ("not_started", "未開始"),
        ("in_progress", "学習中"),
        ("done", "完了"),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progresses")
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.lesson.title} - {self.get_status_display()} ({self.date})"

