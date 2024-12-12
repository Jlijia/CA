import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization







# # 初始界面
# def index(request):
#     return render(request, 'ca_server/interface.html')
#
# #提交CSR证书
# def generate_public_key():
#     """生成RSA密钥对并返回公钥"""
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048
#     )
#     public_key = private_key.public_key()
#     public_key_pem = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     ).decode('utf-8')
#     return public_key_pem
#
#
# def submit_csr(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         gender = request.POST.get('gender')
#         public_key = request.POST.get('public_key')
#         # 保存CSR到服务器（模拟行为）
#         csr_filename = f"{name}_csr.txt"
#         csr_content = f"Name: {name}\nGender: {gender}\nPublic Key:\n{public_key}"
#         csr_path = os.path.join('csr_files', csr_filename)
#         os.makedirs('csr_files', exist_ok=True)
#         with open(csr_path, 'w') as csr_file:
#             csr_file.write(csr_content)
#         return HttpResponse("CSR文件已成功提交！")
#
#     # 生成公钥并渲染页面
#     public_key = generate_public_key()
#     return render(request, 'ca_server/submit_csr.html', {'public_key': public_key})
#
#
#
# def approve_csr(request):
#     return render(request, 'ca_server/approve_csr.html')
#
# def view_certificates(request):
#     return render(request, 'ca_server/view_certificates.html')
#
# def search_certificates(request):
#     return render(request, 'ca_server/search_certificates.html')
#
# def revoke_certificate(request):
#     return render(request, 'ca_server/revoke_certificate.html')
#
# def validate_certificate(request):
#     return render(request, 'ca_server/validate_certificate.html')





from django.shortcuts import render, redirect
from .models import Certificate
from django.http import HttpResponse
from django.utils import timezone

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization
import datetime
import os
from django.conf import settings
from django.template import loader
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

# 客户端提交 CSR 文件
def submit_csr(request):
    if request.method == 'POST':
        # 获取上传的 CSR 文件
        csr_file = request.FILES['csr_file']
        csr_content = csr_file.read().decode('utf-8')

        # 创建 Certificate 对象并保存
        certificate = Certificate(name='New Certificate', csr=csr_content, date_issued=timezone.now())
        certificate.save()

        return redirect('ca_server:review_certificate', certificate_id=certificate.id)
    return render(request, 'ca_client/index.html')  # 客户端提交 CSR 页面


# 审核证书申请
def review_certificate(request, certificate_id):
    certificate = Certificate.objects.get(id=certificate_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            # 签发证书
            certificate.status = 'Issued'
            certificate.save()
            return HttpResponse("证书已签发")
        elif 'reject' in request.POST:
            # 拒绝证书申请
            certificate.status = 'Rejected'
            certificate.save()
            return HttpResponse("证书申请被拒绝")

    return render(request, 'ca_server/review_certificate.html', {'certificate': certificate})  # 服务器端证书审核详情页面



@csrf_exempt
def sign_csr(request):
    if request.method == "POST":
        try:
            # 获取CSR文件内容
            csr_data = request.FILES.get("csr_file")
            if not csr_data:
                return JsonResponse({"error": "CSR file is required."}, status=400)

            # 读取CSR内容并解析
            csr = x509.load_pem_x509_csr(csr_data.read())

            # 校验CSR文件的合法性
            if not csr.is_signature_valid:
                return JsonResponse({"error": "Invalid CSR signature."}, status=400)

            # 签发证书
            ca_key_path = os.path.join(settings.BASE_DIR, "templates\ca\ca_key.pem")
            ca_cert_path = os.path.join(settings.BASE_DIR, "templates\ca\ca_cert.pem")


            with open(ca_key_path, "rb") as key_file, open(ca_cert_path, "rb") as cert_file:
                ca_key = load_pem_private_key(key_file.read(), password=None)
                ca_cert = x509.load_pem_x509_certificate(cert_file.read())

            issued_cert = (
                x509.CertificateBuilder()
                .subject_name(csr.subject)
                .issuer_name(ca_cert.subject)
                .public_key(csr.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.datetime.utcnow())
                .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
                .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
                .sign(private_key=ca_key, algorithm=hashes.SHA256())
            )

            # 保存
            cert_path = os.path.join(settings.BASE_DIR+"/templates/certificates")
            serial_number = issued_cert.serial_number     # 提取序列号

            with open(cert_path + f"/{serial_number}.cer", mode='wb') as cert_file:
                cert_file.write(issued_cert.public_bytes(serialization.Encoding.PEM))
            with open(cert_path + f"/{serial_number}.pem", "wb") as cert_file:
                cert_file.write(issued_cert.public_bytes(encoding=serialization.Encoding.PEM))

            return JsonResponse({"message": "Certificate issued successfully.", "certificate_path": cert_path})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def verify_certificate(request):
    if request.method == "POST":
        try:
            # 获取证书文件内容
            cert_data = request.FILES.get("certificate_file")
            if not cert_data:
                return JsonResponse({"error": "Certificate file is required."}, status=400)

            # 读取证书内容并解析
            cert = x509.load_pem_x509_certificate(cert_data.read(), default_backend())

            # 获取CA证书路径
            ca_cert_path = os.path.join(settings.BASE_DIR, "templates/ca/ca_cert.pem")

            with open(ca_cert_path, "rb") as cert_file:
                ca_cert = x509.load_pem_x509_certificate(cert_file.read(), default_backend())

            # 验证证书签名
            public_key = ca_cert.public_key()
            try:
                # 使用CA证书的公钥验证签名
                public_key.verify(
                    cert.signature,
                    cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
            except Exception as e:
                return JsonResponse({"error": f"Certificate signature verification failed: {str(e)}"}, status=400)

            # 验证证书的有效期
            if cert.not_valid_before > datetime.datetime.utcnow() or cert.not_valid_after < datetime.datetime.utcnow():
                return JsonResponse({"error": "Certificate is expired or not yet valid."}, status=400)

            # 证书的颁发者和主题一致性
            if cert.issuer != ca_cert.subject:
                return JsonResponse({"error": "Certificate issuer does not match the CA."}, status=400)

            return JsonResponse({"message": "Certificate is valid."})

        except Exception as e:
            return JsonResponse({"error": f"Verification failed: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)

