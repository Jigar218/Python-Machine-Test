from django.urls import path, include
from .views import UserCreateView, ClientViewSet, ProjectViewSet, UserProjectsView
from rest_framework.routers import DefaultRouter

# Create a router and register a viewsets
router = DefaultRouter()
router.register(r'clients', ClientViewSet)  # Automatically creates routes for client actions

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),  # User registration
    path('clients/<int:client_id>/projects/', ProjectViewSet.as_view({'post': 'create'}), name='client-projects'),  # Create project for a specific client
    path('clients/<int:client_id>/projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='client-project-detail'),  # Retrieve, update, delete project
    path('projects/', UserProjectsView.as_view(), name='user-projects'),  # New endpoint to list user's projects
]

# Add the router URLs to urlpatterns
urlpatterns += router.urls
