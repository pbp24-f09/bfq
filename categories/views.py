from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from main.models import Product

# Create your views here.
def show_categories(request):
    return render(request, 'categories.html')