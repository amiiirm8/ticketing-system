from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'', MessageViewSet, basename='message')

app_name = 'conversations'

# Versioning handled in project URLs
urlpatterns = [
    path('', include(router.urls)),
]