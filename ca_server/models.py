from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    csr = models.TextField(default='')  # Add default value for existing rows
    status = models.CharField(max_length=50, default='Pending')
    date_issued = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    issuer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

