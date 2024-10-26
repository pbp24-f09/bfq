from django.http import HttpResponse, JsonResponse
from discussion.models import Discussion, Response
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import datetime
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from main.models import Product
import json
#IMPORT BUAT USER PURA PURAAN
from django.contrib.auth.models import User

# Create your views here.
def show_discussion(request):
    discussion = Discussion.objects.all()
    response = Response.objects.all()
    last_login = request.COOKIES['last_login']
    parsed_date_time = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S.%f')
    formatted_without_ms = parsed_date_time.strftime('%Y-%m-%d %H:%M:%S')
    context = {
        'user' : request.user,
        'name':request.user.username,
        'discussion' : discussion,
        'response': response,
        'last_login': formatted_without_ms,
    }
    return render(request, "discussion.html", context)
