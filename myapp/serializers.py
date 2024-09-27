from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User


class ProjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']  # Adjust based on your Project model fields

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    projects = ProjectSimpleSerializer(many=True, read_only=True)  # Include projects
    updated_at = serializers.DateTimeField(read_only=True)  # Add 'updated_at' field

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'updated_at', 'created_by', 'projects']
        read_only_fields = ['created_by', 'created_at', 'updated_at']  # 'created_at' and 'updated_at' are read-only

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Remove 'projects' field if the request is POST, PUT, or if it's a GET request for the list of clients
        if request:
            if request.method in ['POST', 'PUT'] or (request.method == 'GET' and self.context.get('view').action == 'list'):
                representation.pop('projects', None)
            if request.method in ['POST', 'GET']:
                representation.pop('updated_at', None)

        return representation
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    client = serializers.CharField(source='client.client_name', read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']

    def create(self, validated_data):   
        users_data = self.initial_data.get('users', [])
        user_ids = [user['id'] for user in users_data]
        users = User.objects.filter(id__in=user_ids)

        project = Project.objects.create(**validated_data)
        project.users.set(users)  # Associate users with the project
        return project
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Check if the request is a GET request for the list of clients or a POST/PUT request
        if request:

            if request.method == 'GET' and request.path.endswith('/projects/'):
                # You can also add additional conditions if needed
                representation.pop('client', None)
                representation.pop('users', None)

        return representation