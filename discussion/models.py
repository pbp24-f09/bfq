from django.db import models
from main.models import Product
from django.conf import settings

# Create your models here.
class Discussion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.CharField(max_length=100)
    comment = models.TextField()

class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    response_to = models.ForeignKey(Discussion, on_delete=models.CASCADE,)
    response = models.TextField()
