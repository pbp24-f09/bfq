from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    restaurant = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact = models.IntegerField()
    
    @property
    def is_price_valid(self):
        return self.price > 0