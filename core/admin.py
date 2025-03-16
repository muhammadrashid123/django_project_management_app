from django.contrib import admin
from .models import Project, ProjectUserRole, Comment

admin.site.register(Project)
admin.site.register(ProjectUserRole)
admin.site.register(Comment)
