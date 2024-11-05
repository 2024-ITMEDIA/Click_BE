from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=10)  # 작성자 이름
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간 자동 저장

    def __str__(self):
        return f'{self.name} - {self.created_at}'

