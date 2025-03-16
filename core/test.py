from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Project, ProjectUserRole

User = get_user_model()

class ProjectRBACAPITest(TestCase):
    """Test Role-Based Access Control for Project API"""

    def setUp(self):
        """Set up test users and projects"""
        self.client = APIClient()

        self.owner = User.objects.create_user(username="owner", email="owner@example.com", password="password123")
        self.editor = User.objects.create_user(username="editor", email="editor@example.com", password="password123")
        self.reader = User.objects.create_user(username="reader", email="reader@example.com", password="password123")
        self.no_role = User.objects.create_user(username="norole", email="norole@example.com", password="password123")

        # Create a project
        self.project = Project.objects.create(name="Test Project", description="Project for testing", owner=self.owner)

        # Assign roles
        ProjectUserRole.objects.create(user=self.owner, project=self.project, role="owner")
        ProjectUserRole.objects.create(user=self.editor, project=self.project, role="editor")
        ProjectUserRole.objects.create(user=self.reader, project=self.project, role="reader")

        # Get authentication tokens
        self.client.force_authenticate(user=self.owner)

    def test_owner_can_create_project(self):
        """Test that an owner can create a project"""
        data = {"name": "New Project", "description": "Created by owner"}
        response = self.client.post("/api/projects/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_editor_cannot_create_project(self):
        """Test that an editor cannot create a project"""
        self.client.force_authenticate(user=self.editor)
        data = {"name": "New Project", "description": "Created by editor"}
        response = self.client.post("/api/projects/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_cannot_create_project(self):
        """Test that a reader cannot create a project"""
        self.client.force_authenticate(user=self.reader)
        data = {"name": "New Project", "description": "Created by reader"}
        response = self.client.post("/api/projects/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_role_cannot_create_project(self):
        """Test that a user with no role cannot create a project"""
        self.client.force_authenticate(user=self.no_role)
        data = {"name": "New Project", "description": "Created by no role user"}
        response = self.client.post("/api/projects/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_can_view_project(self):
        """Test that a reader can view project details"""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editor_can_edit_project(self):
        """Test that an editor can edit the project details"""
        self.client.force_authenticate(user=self.editor)
        data = {"name": "Updated Project", "description": "Updated by editor"}
        response = self.client.put(f"/api/projects/{self.project.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reader_cannot_edit_project(self):
        """Test that a reader cannot edit the project"""
        self.client.force_authenticate(user=self.reader)
        data = {"name": "Updated Project", "description": "Updated by reader"}
        response = self.client.put(f"/api/projects/{self.project.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_cannot_delete_project(self):
        """Test that an editor cannot delete the project"""
        self.client.force_authenticate(user=self.editor)
        response = self.client.delete(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_cannot_delete_project(self):
        """Test that a reader cannot delete the project"""
        self.client.force_authenticate(user=self.reader)
        response = self.client.delete(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_project(self):
        """Test that the owner can delete the project"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
