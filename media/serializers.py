# media/serializers.py
from rest_framework import serializers
from .models import Image, Team  # 모델을 가져옴
from .models import ProjectDetail

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'project_name', 'team_name', 'members'] #'project_intro', 'design_intent']  # 팀 관련 필드

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = ['id', 'team', 'project_intro', 'design_intent']  # 포함할 필드 정의
        
class ImageSerializer(serializers.ModelSerializer):
    team = TeamSerializer(required=False)  # 필수가 아닌 필드로 설정
    
    class Meta:
        model = Image  # 사용할 모델
        fields = ['id', 'image', 'team']  # 직렬화할 필드
