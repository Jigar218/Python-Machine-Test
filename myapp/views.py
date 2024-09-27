from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.models import User

# Custom permission to check if the user is the owner of the object
class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of the object to update or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

# User Creation View
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Client ViewSet
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        client = self.get_object()  # Get the client instance
        self.check_object_permissions(request, client)
        serializer = self.get_serializer(client)  # Serialize client instance
        return Response(serializer.data)  # Return the serialized data

# Project ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        client_id = self.kwargs['client_id']
        client = get_object_or_404(Client, id=client_id)
        
        users_data = self.request.data.get('users', [])
        user_ids = [user['id'] for user in users_data]
        users = User.objects.filter(id__in=user_ids)

        project = serializer.save(client=client, created_by=self.request.user)
        project.users.set(users)

        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # If client_id is specified, filter projects by client; otherwise, return all projects created by the user
        client_id = self.kwargs.get('client_id', None)
        if client_id:
            return Project.objects.filter(client__id=client_id, client__created_by=self.request.user)
        return Project.objects.filter(created_by=self.request.user)  # Filter projects by the logged-in user

    def retrieve(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id, client__id=client_id)

        self.check_object_permissions(request, project)  
        return Response(ProjectSerializer(project).data)

# New view to list all projects for the logged-in user
class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)
