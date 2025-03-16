from rest_framework.permissions import BasePermission
from core.models import ProjectUserRole, Comment, Project

class IsOwnerOrEditorOrReader(BasePermission):
    """
    Role-Based Access Control:
    - Owners & Editors can modify projects.
    - Owners & Editors can create/edit/delete comments.
    - Owners, Editors, and Readers can view projects and comments.
    - Readers cannot create or modify anything.
    - Users with no role cannot access anything.
    """

    def has_object_permission(self, request, view, obj):
        """
        - Owners & Editors can create/edit/delete comments.
        - Owners, Editors, and Readers can view comments.
        - Owners & Editors can modify projects.
        - Readers can only view projects.
        """
        # If the object is a Comment get the related project
        if isinstance(obj, Comment):
            project = obj.project
            user_role = project.members.filter(user=request.user).first()
            if not user_role:
                return False  # No role, no access

            # Ownrs & Editors can create/edit/delete comments
            if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                return user_role.role in ["owner", "editor"]

            # Owners, Editors, and Readers can view comments
            return user_role.role in ["owner", "editor", "reader"]

        # If it is a Project, allow Readrs to view, but prevent modifications
        if isinstance(obj, Project):
            user_role = obj.members.filter(user=request.user).first()
            if not user_role:
                return False  # No role, no access

            # Readers can only view projects
            if request.method in ["GET", "HEAD", "OPTIONS"]:
                return True  # Readers can read project details

            # Owners & Editors can modify the project but Readers cannot
            return user_role.role in ["owner", "editor"]

        return False  # Default deny

class IsOwner(BasePermission):
    """
    Custom permission:
    - Only Owners can manage user roles and delete projects.
    """

    def has_object_permission(self, request, view, obj):
        """
        - Owners can manage user roles and delete projects.
        - Editors & Readers cannot perform these actions.
        """
        # Check if obj is a Project or ProjectUserRole
        project = obj.project if isinstance(obj, ProjectUserRole) else obj
        user_role = project.members.filter(user=request.user).first()
        return user_role and user_role.role == "owner"
