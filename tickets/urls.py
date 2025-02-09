from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet

router = DefaultRouter()
router.register(r'', TicketViewSet, basename='ticket')

# Centralized version prefix handled in project urls.py
urlpatterns = [
    path('', include(router.urls)),
]