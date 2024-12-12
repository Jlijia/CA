from django.db import models

class UserCertificate(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    public_key = models.TextField()
    state = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Revoked', 'Revoked')])
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
