from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')  # 최신순으로 정렬
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # 누구나 접근 가능
    http_method_names = ['get', 'post']  # 조회(get)와 등록(post)만 허용
