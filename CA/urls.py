from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ca_server.urls')),  # 默认指向 ca_server 应用
]
