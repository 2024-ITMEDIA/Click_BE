# media/serializers.py
from rest_framework import serializers
from .models import Image  # 모델을 가져옴

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image  # 사용할 모델
        fields = ['id', 'image']  # 직렬화할 필드