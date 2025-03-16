from rest_framework import serializers
from .models import Project, Comment, ProjectUserRole

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']
        read_only_fields = ['id', 'created_at', 'owner']


class ProjectUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUserRole
        fields = '__all__'
