from rest_framework import serializers
from .models import Team, ProjectDetail, TeamImage, Image

class TeamSerializer(serializers.ModelSerializer):
    # members를 DictField로 처리, value는 ListField로 처리
    members = serializers.DictField(child=serializers.ListField(child=serializers.CharField(max_length=100)))
    

    class Meta:
        model = Team
        fields = ['id', 'project_name', 'team_name', 'members', 'project_image']  # team_image -> project_image로 변경


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamImage
        fields = ['id', 'image']

class ProjectDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer()  # 팀 정보 포함

    class Meta:
        model = ProjectDetail
        fields = ['id', 'project_intro', 'design_intent', 'team']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'team_image', 'team_name']  # team_image 필드로 수정

class ProjectListSerializer(serializers.ModelSerializer):
    team = TeamSerializer()  # 팀 정보 포함

    class Meta:
        model = ProjectDetail
        fields = ['id', 'team']

    def to_representation(self, instance):
        # ProjectListView에서는 members에서 키만 반환
        representation = super().to_representation(instance)

        # `members`는 딕셔너리이므로, 그 키만 반환
        team_members = representation['team']['members']
        representation['team']['members'] = list(team_members.keys())  # 키만 리스트로 변환

        return representation
