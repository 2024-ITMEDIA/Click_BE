# admin.py
from django.contrib import admin
from .models import Team, ProjectDetail, TeamImage, Image

admin.site.register(Team)
admin.site.register(ProjectDetail)
admin.site.register(TeamImage)
admin.site.register(Image)
