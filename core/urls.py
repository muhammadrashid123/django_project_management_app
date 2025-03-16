from rest_framework import routers
from django.urls import path, include
from .views import ProjectViewSet, ProjectUserRoleViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'roles', ProjectUserRoleViewSet, basename='roles')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
