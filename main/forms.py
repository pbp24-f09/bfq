from django.forms import ModelForm
from main.models import Food

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "price", "restaurant", "location", "contact"]