from django.db import models
import json

class Team(models.Model):
    project_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)  # 여전히 team_name은 팀 이름을 저장
    members = models.JSONField()  # JSONField로 변경하여 리스트 형태로 저장
    team_image = models.ImageField(upload_to='team_images/', null=True, blank=True)  # 팀 이미지 필드 추가

    def __str__(self):
        return self.team_name  # team_name을 팀의 이름으로 출력


class ProjectDetail(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='project_details')  # 외래키로 연결
    project_intro = models.TextField()  # 작품 소개
    design_intent = models.TextField()  # 기획 의도

    def __str__(self):
        return f"ProjectDetail - {self.team.team_name}"  # 팀 이름을 포함하여 출력
    
class ProjectImage(models.Model):
    project_detail = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='project_images/')


class Image(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    team = models.ForeignKey(Team, related_name='images', on_delete=models.CASCADE, null=True, blank=True)  # 외래키로 연결
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        # team_name을 통해 팀을 찾아서 연결할 필요 없음
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team.team_name} - Image"  # team_name으로 출력
