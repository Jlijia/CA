# ca_client/urls.py
from django.urls import path
from . import views

app_name = 'ca_client'

urlpatterns = [
    path('', views.index, name='index'),  # 根 URL 映射到 index 视图
    path('enter_system/', views.enter_system, name='enter_system'),  # 进入系统页面
]
