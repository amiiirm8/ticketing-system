from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer
)
from .models import CustomUser
from .permissions import IsOwnerOrAdmin

class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH: Retrieve or update authenticated user's profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        return self.request.user

class RegisterView(generics.CreateAPIView):
    """
    POST: Create new user account with email/password
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    """
    POST: Obtain JWT access/refresh tokens for authentication
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    """
    GET: List all users (admin only)
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]