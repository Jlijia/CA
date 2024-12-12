from django.urls import path
from . import views

app_name = 'ca_server'

urlpatterns = [
    path('api/sign_csr', views.sign_csr, name='sign_csr'),
    path('upload_csr', views.upload_csr, name='upload_csr'),
    path('api/verify_certificate', views.verify_certificate, name='verify_certificate'),
]
