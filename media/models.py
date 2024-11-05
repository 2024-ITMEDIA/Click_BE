# media/models.py
from django.db import models

class Team(models.Model):
    project_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    members = models.JSONField()  # 역할과 함께 멤버를 저장하기 위해 JSONField 사용

    def __str__(self):
        return self.team_name
    
class ProjectDetail(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='project_details')
    project_intro = models.TextField()  # 작품 소개
    design_intent = models.TextField()  # 기획 의도

class Image(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)  # null=True 추가
    team = models.ForeignKey(Team, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.team.project_name} - Image" if self.team else "Image without team"
