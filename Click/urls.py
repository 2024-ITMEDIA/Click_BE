"""
URL configuration for Click project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # 리다이렉트 뷰를 추가
from django.conf import settings
from . import views  # views 모듈 임포트
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('media.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),  # 루트 URL을 api/로 리다이렉트
    path('comment/', include('comment.urls')),
    path('health/', views.health_check, name='health_check'),
    
    path('api/', RedirectView.as_view(url='/api/projects/', permanent=False)),  # 수정된 부분
]
