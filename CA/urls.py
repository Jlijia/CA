from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ca_server.urls')),  # 根 URL 映射到 ca_client 应用
]
