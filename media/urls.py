# media/urls.py
from django.urls import path
from .views import ImageUploadView, ImageListView, ProjectListView, ProjectDetailView

urlpatterns = [
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),# 이미지 업로드
    path('images/', ImageListView.as_view(), name='image-list'), # 이미지 목록 보기
    path('projects/', ProjectListView.as_view(), name='project-list'),# 프로젝트 목록 보기 (프로젝트 이름,프로젝트 사진, 팀명, 팀원만 포함)
    path('project-detail/<int:project_id>/', ProjectDetailView.as_view(), name='project-detail'), # 프로젝트 상세보기 (프로젝트의 작품 소개, 기획 의도, 팀명, 팀 이미지 등 포함)
]
