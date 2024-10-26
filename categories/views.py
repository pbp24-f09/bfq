from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from main.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

# Create your views here.
def show_categories(request):
    return render(request, 'categories.html')

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    restaurant = strip_tags(request.POST.get("restaurant"))
    location = strip_tags(request.POST.get("location"))
    contact = strip_tags(request.POST.get("contact"))
    image = request.FILES.get("image")
    user = request.user
    
    new_product = Product(
        name=name, 
        price=price,
        restaurant=restaurant,
        location=location,
        contact=contact,
        image=image,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)
