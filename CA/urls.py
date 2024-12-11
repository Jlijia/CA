from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ca_client.urls')),  # 根 URL 映射到 ca_client 应用
]
