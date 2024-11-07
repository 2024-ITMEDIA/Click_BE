# admin.py
from django.contrib import admin
from .models import Team, ProjectDetail, ProjectImage, Image

admin.site.register(Team)
admin.site.register(ProjectDetail)
admin.site.register(ProjectImage)
#admin.site.register(Image)