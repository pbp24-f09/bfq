from django.db import models
import uuid

class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    restaurant = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact = models.IntegerField()
    
    @property
    def is_price_valid(self):
        return self.price > 0