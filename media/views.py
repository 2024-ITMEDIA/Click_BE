from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image, ProjectDetail, TeamImage
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageSerializer, TeamSerializer, ProjectDetailSerializer, ProjectListSerializer

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # 텍스트 데이터 가져오기
        team_data = {
            "project_name": request.data.get('team[project_name]'),
            "team_name": request.data.get('team[team_name]'),
        }

        # 'team[members]'는 여러 개가 올 수 있으므로, 이를 리스트로 수집
        members = request.data.get('team[members]')  # 여기서 JSON 형태로 멤버 데이터를 받습니다.
        if members:
            team_data["members"] = members  # 리스트 형태로 members 저장
        else:
            return Response({"errors": "No team members provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 텍스트 데이터가 부족하면 오류 응답
        if not all(team_data.values()):
            return Response({"errors": "No team data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # TeamSerializer로 팀 정보 처리
        team_serializer = TeamSerializer(data=team_data)
        if team_serializer.is_valid():
            team = team_serializer.save()
        else:
            return Response({"errors": team_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # 프로젝트 상세 정보 처리
        project_detail_data = {
            "project_intro": request.data.get('project_intro'),
            "design_intent": request.data.get('design_intent'),
            "team": team.id,
        }

        # ProjectDetailSerializer로 프로젝트 상세 정보 처리
        project_detail_serializer = ProjectDetailSerializer(data=project_detail_data)
        if project_detail_serializer.is_valid():
            project_detail_serializer.save()
        else:
            return Response({"errors": project_detail_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 파일 처리
        image_file = request.FILES.get('image')  # 이미지 파일은 `request.FILES`에서 가져옴
        if not image_file:
            return Response({"errors": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # ImageSerializer로 이미지 처리
        image_data = {
            'team_image': image_file,  # 팀 이미지는 이제 `team_image` 필드로 처리
            'team_name': request.data.get('team_name'),  # team_name을 추가
        }

        # 팀 이미지를 `Image` 모델의 `team_image` 필드에 저장
        image_serializer = ImageSerializer(data=image_data)  # team_name을 포함하여 이미지 처리
        if image_serializer.is_valid():
            image = image_serializer.save()  # 팀 정보와 연결하여 저장
            return Response({
                "message": "Image uploaded successfully",
                "image_id": image.id,
                "image_url": image.team_image.url,  # team_image URL을 반환
                "team_name": image.team_name,
                "project_detail": project_detail_serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response({"errors": image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class ProjectListView(APIView):
    def get(self, request):
        project_details = ProjectDetail.objects.all()
        serializer = ProjectListSerializer(project_details, many=True)
        return Response(serializer.data)


class ProjectDetailView(APIView):
    def get(self, request, project_id, format=None):
        try:
            # 프로젝트 상세 정보를 가져오기 (프로젝트 아이디로 조회)
            project_detail = ProjectDetail.objects.get(id=project_id)

            # 관련된 팀 이미지들 가져오기 (ProjectDetail -> TeamImage)
            team_images = TeamImage.objects.filter(project_detail=project_detail)

            # 프로젝트 상세 정보 직렬화
            project_detail_serializer = ProjectDetailSerializer(project_detail)

            # 직렬화된 프로젝트 데이터를 가져옵니다.
            project_data = project_detail_serializer.data

            # 팀 이미지 URLs을 가져옵니다. TeamImage 모델에 있는 `image` 필드를 URL로 변환하여 반환
            project_data['team_images'] = [
                team_image.image.url for team_image in team_images
            ]

            # 반환할 데이터에 팀원 데이터 추가
            team_members = project_data['team']['members']
            project_data['team']['members'] = team_members  # 딕셔너리 형태 그대로 반환

            return Response(project_data, status=status.HTTP_200_OK)

        except ProjectDetail.DoesNotExist:
            return Response({"error": "ProjectDetail not found."}, status=status.HTTP_404_NOT_FOUND)
