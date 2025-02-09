from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin  # Add this import
from rest_framework import permissions  # Add this import


schema_view = get_schema_view(
    openapi.Info(
        title="Ticketing System API",
        default_version='v1',
        description="API documentation for Ticketing System",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Add this line
    patterns=[
        path('api/v1/', include([
            path('accounts/', include('accounts.urls')),
            path('tickets/', include('tickets.urls')),
            path('tickets/<int:ticket_pk>/messages/', include('conversations.urls')),
        ])),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('accounts/', include('accounts.urls')),
        path('tickets/', include('tickets.urls')),
        path('tickets/<int:ticket_pk>/messages/', include('conversations.urls')),
    ])),
    
    # Swagger/ReDoc - move these outside api/v1
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]