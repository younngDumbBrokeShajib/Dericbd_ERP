from django.db import models

# Create your models here.
class Contacts(models.Model):
    address = models.TextField()
    taxId = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    tags = models.CharField(max_length=1024)