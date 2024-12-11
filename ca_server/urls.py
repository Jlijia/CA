from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 设置默认页面为 home
]
