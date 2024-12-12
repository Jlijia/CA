# Generated by Django 5.0.6 on 2024-12-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='用户名')),
                ('common_name', models.CharField(max_length=255, verbose_name='公共名')),
                ('public_key', models.TextField(verbose_name='公钥')),
                ('serial_number', models.CharField(max_length=64, unique=True, verbose_name='序列号')),
                ('issued_at', models.DateTimeField(auto_now_add=True, verbose_name='签发时间')),
                ('expires_at', models.DateTimeField(verbose_name='过期时间')),
                ('status', models.CharField(choices=[('valid', '有效'), ('revoked', '已注销'), ('expired', '已过期')], default='valid', max_length=10, verbose_name='状态')),
            ],
        ),
    ]
