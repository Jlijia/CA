from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 默认界面
    path('submit_csr/', views.submit_csr, name='submit_csr'),
    path('approve_csr/', views.approve_csr, name='approve_csr'),
    path('view_certificates/', views.view_certificates, name='view_certificates'),
    path('search_certificates/', views.search_certificates, name='search_certificates'),
    path('revoke_certificate/', views.revoke_certificate, name='revoke_certificate'),
    path('validate_certificate/', views.validate_certificate, name='validate_certificate'),
]
