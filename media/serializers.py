from rest_framework import serializers
from .models import Team, ProjectDetail, ProjectImage, Image

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.CharField(max_length=100)  # 멤버 이름을 문자열로 처리
    )

    class Meta:
        model = Team
        fields = ['id', 'project_name', 'team_name', 'members', 'team_image']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer()  # 팀 정보 포함
    project_images = ProjectImageSerializer(many=True, read_only=True)  # 프로젝트 이미지 포함

    class Meta:
        model = ProjectDetail
        fields = ['id', 'project_intro', 'design_intent', 'project_images', 'team']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'team_name']

class ProjectListSerializer(serializers.ModelSerializer):
    team = TeamSerializer()  # 팀 정보 포함
    project_images = ProjectImageSerializer(many=True, read_only=True)  # 프로젝트 이미지 포함

    class Meta:
        model = ProjectDetail
        fields = ['id', 'team', 'project_images']
