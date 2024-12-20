from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from main.models import Product
from main.forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Q
import json

# Create your views here.
def show_categories(request):
    return render(request, 'categories.html')

@login_required(login_url='/login')
def show_categories_admin(request):
    return render(request, 'categories_admin.html')

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_product_ajax_cat(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    restaurant = strip_tags(request.POST.get("restaurant"))
    location = strip_tags(request.POST.get("location"))
    contact = strip_tags(request.POST.get("contact"))
    cat = request.POST.get("cat")
    image = request.FILES.get("image")
    user = request.user
    
    new_product = Product(
        name=name, 
        price=price,
        restaurant=restaurant,
        location=location,
        contact=contact,
        cat=cat,
        image=image,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/login')
def edit_product_cat(request, id):
    product = Product.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('categories:show_categories_admin')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form})

@login_required(login_url='/login')
def delete_product_cat(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('categories:show_categories_admin'))

@csrf_exempt
def search_filter(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        query = body.get('value', '')
        selected_range = body.get('range', [])
        selected_cat = body.get('category', [])
        selected_order = body.get('order', '')

        products = Product.objects.all()

        if query:
            products = products.filter(Q(name__icontains=query) | Q(restaurant__icontains=query))
        
        if selected_range:
            filter_price = Q()
            if "Less than 50.000" in selected_range:
                filter_price |= Q(price__lt=50000)
            if "50.000 - 100.000" in selected_range:
                filter_price |= Q(price__gte=50000) & Q(price__lte=100000)
            if "100.000 - 150.000" in selected_range:
                filter_price |= Q(price__gte=100000) & Q(price__lte=150000)
            if "More than 150.000" in selected_range:
                filter_price |= Q(price__gt=150000)

            products = products.filter(filter_price)

        if selected_cat:
            # products = products.filter(Q(cat__icontains=selected_cat))
            filter_category = Q()
            for cat in selected_cat:
                filter_category |= Q(cat__icontains=cat)
            
            products = products.filter(filter_category)
        
        if (selected_order):
            if selected_order == "Highest":
                products = products.order_by("-price")
            elif selected_order == "Lowest":
                products = products.order_by("price")

        return HttpResponse(serializers.serialize("json", products), content_type="application/json")
    
    return HttpResponse({"error": "Invalid request"}, status=400)