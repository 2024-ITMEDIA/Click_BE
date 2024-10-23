from rest_framework import generics
from .models import Image
from .serializers import ImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render #프론트엔드 확인
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # 파일 업로드를 위한 파서 설정

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()  # 저장된 이미지 객체
            return Response({
                "message": "Image uploaded successfully",
                "image_id": image.id,  # 이미지 ID 반환
                "image_url": image.image.url  # 이미지 URL 반환 (media 설정에 따라)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'image/index.html')
#프론트엔드에서 확인을 위한 코드