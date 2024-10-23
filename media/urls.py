# media/urls.py
from django.urls import path
from .views import ImageCreateView, index,  ImageListView, ImageUploadView

# Click_BE/urls.py
urlpatterns = [
    path('', index, name='index'), #프론트엔드를 위해 씀
    path('images/', ImageCreateView.as_view(), name='image-create'),
    path('api/images/', ImageListView.as_view(), name='image-list'),
    path('api/images/upload/', ImageUploadView.as_view(), name='image-upload'),
]
