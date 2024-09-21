from django.contrib import admin
from django.urls import path, include
# Import necessário para a documentação da API usando o Swagger (drf-yasg)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração da documentação Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Traffic Monitoring API",  # Título da documentação
      default_version='v1',            # Versão da API
      description="API Traffic"  # Descrição da API
   ),
   public=True,  # Disponibiliza a documentação publicamente
   permission_classes=[permissions.AllowAny],  # Permissões para aceder à documentação
)

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para o admin do Django
    path('api/', include('traffic_api.urls')),  # Inclui as URLs da aplicação traffic_api
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Documentação da API
]
