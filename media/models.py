from django.db import models
import json

# models.py
class Team(models.Model):
    project_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    members = models.JSONField()
    project_image = models.ImageField(upload_to='project_images/', null=True, blank=True)  

    def __str__(self):
        return self.team_name



    def __str__(self):
        return self.team_name  # team_name을 팀의 이름으로 출력


class ProjectDetail(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='project_details')  # 외래키로 연결
    project_intro = models.TextField()  # 작품 소개
    design_intent = models.TextField()  # 기획 의도

    def __str__(self):
        return f"ProjectDetail - {self.team.team_name}"  # 팀 이름을 포함하여 출력
    
class TeamImage(models.Model):  # 이름 변경
    project_detail = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE, related_name='team_images')
    image = models.ImageField(upload_to='team_images/')  # 프로젝트 이미지

    def __str__(self):
        return f"TeamImage for {self.project_detail.team.team_name}"


class Image(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    team = models.ForeignKey(Team, related_name='images', on_delete=models.CASCADE, null=True, blank=True)  # 외래키로 연결
    team_image = models.ImageField(upload_to='images/')  # team_image로 역할 변경

    def save(self, *args, **kwargs):
        # team_name을 통해 팀을 찾아서 연결할 필요 없음
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team.team_name} - Image"  # team_name으로 출력
