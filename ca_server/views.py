import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# 初始界面
def index(request):
    return render(request, 'ca_server/interface.html')

#提交CSR证书
def generate_public_key():
    """生成RSA密钥对并返回公钥"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return public_key_pem


def submit_csr(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        public_key = request.POST.get('public_key')
        # 保存CSR到服务器（模拟行为）
        csr_filename = f"{name}_csr.txt"
        csr_content = f"Name: {name}\nGender: {gender}\nPublic Key:\n{public_key}"
        csr_path = os.path.join('csr_files', csr_filename)
        os.makedirs('csr_files', exist_ok=True)
        with open(csr_path, 'w') as csr_file:
            csr_file.write(csr_content)
        return HttpResponse("CSR文件已成功提交！")

    # 生成公钥并渲染页面
    public_key = generate_public_key()
    return render(request, 'submit_csr.html', {'public_key': public_key})



def approve_csr(request):
    return render(request, 'ca_server/approve_csr.html')

def view_certificates(request):
    return render(request, 'ca_server/view_certificates.html')

def search_certificates(request):
    return render(request, 'ca_server/search_certificates.html')

def revoke_certificate(request):
    return render(request, 'ca_server/revoke_certificate.html')

def validate_certificate(request):
    return render(request, 'ca_server/validate_certificate.html')
