from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Документация для API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)


def index(request):
    return redirect('/silant/machines/')


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('silant/', include('mySilant.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('mySilant.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
