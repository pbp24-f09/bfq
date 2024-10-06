from django.shortcuts import render, redirect
from main.forms import FoodForm
from main.models import Food

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