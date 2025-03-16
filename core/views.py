from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Project, Comment, ProjectUserRole
from .serializers import ProjectSerializer, CommentSerializer, ProjectUserRoleSerializer
from .permissions import IsOwner, IsOwnerOrEditorOrReader
from constants import *
from utils import custom_response


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEditorOrReader]

    def get_permissions(self):
        """Only Owners and Editors can create or modify projects."""
        if self.action in ["create", "update", "destroy"]:
            return [IsOwnerOrEditorOrReader()]
        return super().get_permissions()

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user).distinct()

    def perform_create(self, serializer):
        """Ensure only Owners and Editors can create projects."""
        user_role = ProjectUserRole.objects.filter(user=self.request.user).first()

        if not user_role:
            raise PermissionDenied("You do not have permission to create a project.")
        if user_role.role == "reader":
            raise PermissionDenied("Readers cannot create projects.")

        project = serializer.save(owner=self.request.user)
        ProjectUserRole.objects.create(user=self.request.user, project=project, role="owner")


class ProjectUserRoleViewSet(viewsets.ModelViewSet):
    queryset = ProjectUserRole.objects.all()
    serializer_class = ProjectUserRoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_permissions(self):
        """Only Owners can manage roles (create, update, delete)."""
        if self.action in ["create", "update", "destroy"]:
            return [IsOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        user = serializer.validated_data["user"]

        # Check if the user already has a role in this project
        if ProjectUserRole.objects.filter(user=user, project=project).exists():
            raise ValidationError(ERROR_USER_ALREADY_HAS_ROLE)

        # Only Owners can assign roles
        if not project.members.filter(user=self.request.user, role="owner").exists():
            raise PermissionDenied(ERROR_UNAUTHORIZED_ROLE_ASSIGN)

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Only Owners can remove user roles from a project."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return custom_response(SUCCESS_ROLE_REMOVED, None, status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEditorOrReader]

    def perform_create(self, serializer):
        """Ensure only Owners and Editors can create comments."""
        project = serializer.validated_data["project"]
        user_role = project.members.filter(user=self.request.user).first()

        if not user_role or user_role.role not in ["owner", "editor"]:
            raise PermissionDenied("You do not have permission to add comments.")

        serializer.save(author=self.request.user)
