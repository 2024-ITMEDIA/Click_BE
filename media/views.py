from rest_framework import generics
from .models import Image, ProjectDetail
from .serializers import ImageSerializer, TeamSerializer, ProjectDetailSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # 파일 업로드를 위한 파서 설정

    def post(self, request, format=None):
        print("Request data:", request.data)  # 요청 데이터 출력

        # 팀 데이터 구성
        team_data = {
            "project_name": request.data.get('team[project_name]'),
            "team_name": request.data.get('team[team_name]'),
            "members": request.data.get('team[members]'),
        }

        # 팀 데이터가 모두 채워져 있는지 확인
        if not all(team_data.values()):
            return Response({"errors": "No team data provided"}, status=status.HTTP_400_BAD_REQUEST)

        team_serializer = TeamSerializer(data=team_data)  # 팀 정보 시리얼라이저
        
        if team_serializer.is_valid():
            team = team_serializer.save()  # 팀 정보 저장
        else:
            return Response({"errors": team_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # 프로젝트 세부 정보 처리
        project_detail_data = {
            "project_intro": request.data.get('project_intro'),  # 프로젝트 소개
            "design_intent": request.data.get('design_intent'),  # 기획 의도
            "team": team.id,  # 팀 ID
        }

        project_detail_serializer = ProjectDetailSerializer(data=project_detail_data)

        if project_detail_serializer.is_valid():
            project_detail_serializer.save()
        else:
            return Response({"errors": project_detail_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 데이터 처리
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image = image_serializer.save(team=team)  # 팀과 함께 이미지 저장
            return Response({
                "message": "Image uploaded successfully",
                "image_id": image.id,
                "image_url": image.image.url,
                "team": team_serializer.data,  # 팀 정보 반환
                "project_detail": project_detail_serializer.data,  # 프로젝트 세부 정보 반환
            }, status=status.HTTP_201_CREATED)

        print("Image serializer errors:", image_serializer.errors)  # 직렬화 오류 출력
        return Response({"errors": image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    def get(self, request, team_id, format=None):
        try:
            project_detail = ProjectDetail.objects.get(team=team_id)  # 특정 팀 ID로 필터링
            serializer = ProjectDetailSerializer(project_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProjectDetail.DoesNotExist:
            return Response({"error": "ProjectDetail not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, team_id, format=None):
        # team_id를 사용하여 프로젝트 세부 정보 생성
        project_detail_data = {
            "project_intro": request.data.get('project_intro'),
            "design_intent": request.data.get('design_intent'),
            "team": team_id  # URL에서 받은 team_id 사용
        }
        
        project_detail_serializer = ProjectDetailSerializer(data=project_detail_data)

        if project_detail_serializer.is_valid():
            project_detail_serializer.save()  # 프로젝트 세부 정보 저장
            return Response(project_detail_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(project_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'image/index.html')  # 프론트엔드에서 확인을 위한 코드
