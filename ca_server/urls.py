from django.urls import path
from . import views

app_name = 'ca_server'

urlpatterns = [
    path('submit_csr/', views.submit_csr, name='submit_csr'),  # 客户端提交 CSR 文件
    path('review_certificate/<int:certificate_id>/', views.review_certificate, name='review_certificate'),  # 审核证书申请
]
