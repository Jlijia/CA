from django.shortcuts import render

# 主页视图
def home(request):
    return render(request, 'ca_server/home.html')
