from django.shortcuts import render

def show_main(request):
    context = {
        'app_name' : 'Bandung Food Quest',
        'tagline' : "Delicious bandung's food",
    }

    return render(request, "main.html", context)