from django.shortcuts import render, redirect
from main.forms import FoodForm
from main.models import Food
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    foods = Food.objects.all()
    
    context = {
        'app_name' : 'Bandung Food Quest',
        'tagline' : "Delicious bandung's food",
    }

    return render(request, "main.html", context)

def create_food(request):
    form = FoodForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_food.html", context)

def show_xml(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Food.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Food.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")