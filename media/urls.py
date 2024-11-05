# media/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ImageCreateView, index,  ImageListView, ImageUploadView, ProjectDetailView

# Click_BE/urls.py
urlpatterns = [
    path('', index, name='index'), #프론트엔드를 위해 씀
    path('images/', ImageCreateView.as_view(), name='image-create'),
    path('api/images/', ImageListView.as_view(), name='image-list'),
    path('api/images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('api/project-detail/<int:team_id>/', ProjectDetailView.as_view(), name='project-detail'),  # 새로운 URL 추가
]

if settings.DEBUG:  # DEBUG가 True일 때만 미디어 파일 제공
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)