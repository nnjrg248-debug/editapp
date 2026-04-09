
from django.db import models

class Memo(models.Model):
    title = models.CharField(max_length=200)  # タイトル（最大200文字）
    content = models.TextField()               # メモ本文
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動設定）
    updated_at = models.DateTimeField(auto_now=True)      # 更新日時（自動設定）

    class Meta:
        db_table='Memo'
        
    def __str__(self):
        return self.title
    
class Post(models.Model):  # ここが Post ではなく Article などの場合
    title = models.CharField(max_length=200)
    content = models.TextField()