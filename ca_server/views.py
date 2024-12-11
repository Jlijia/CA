from django.shortcuts import render, redirect
from .models import Certificate
from django.http import HttpResponse
from django.utils import timezone


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
