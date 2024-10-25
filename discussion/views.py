from django.shortcuts import render
from django.http import HttpResponse
from authentication.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.

@csrf_exempt
@require_POST
def add_mood_entry_ajax(request):
    full_name = request.POST.get("full_name") # Username
    age = request.POST.get("age") # Age

    new_discussion = CustomUser(
        full_name=full_name, age=age,
    )
    new_discussion.save()

    return HttpResponse(b"CREATED", status=201)