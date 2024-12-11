# ca_client/views.py
from django.shortcuts import render

def index(request):
    # 渲染默认页面
    return render(request, 'ca_client/index.html')  # 渲染客户端的 index.html 页面

def enter_system(request):
    # 渲染进入系统后的页面
    return render(request, 'ca_client/enter_system.html')  # 渲染进入系统页面
