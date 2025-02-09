from django.urls import path
from .views import (
    UserDetailView,
    RegisterView,
    LoginView,
    UserListView
)

urlpatterns = [
    # User endpoints
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Admin endpoints
    path('users/', UserListView.as_view(), name='user-list'),
]