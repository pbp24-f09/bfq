from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import uuid

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    CATEGORY_CHOICES = [
        ('BERAT', 'Makanan Berat dan Nasi'),
        ('OLAHAN', 'Olahan Ayam dan Daging'),
        ('MIE', 'Mie, Pasta, dan Spaghetti'),
        ('SNACK', 'Makanan Ringan dan Cemilan'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    restaurant = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    cat = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='FOOD')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    @property
    def is_price_valid(self):
        return self.price > 0
