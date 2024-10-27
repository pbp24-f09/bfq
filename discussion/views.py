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
@login_required(login_url='/login/')
def show_discussion(request):
    discussion = Discussion.objects.all()
    response = Response.objects.all()
    context = {
        'user' : request.user,
        'name':request.user.username,
        'discussion' : discussion,
        'response': response,
    }
    return render(request, "discussion/discussion.html", context)

@login_required(login_url='/login/')
@csrf_exempt
def create_comment(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        comment = request.POST.get('comment')
        date = datetime.now()
        topic = request.POST.get('topic')
        new_comment = Discussion(user = user, product = product, date = date , topic = topic, comment = comment)
        # result = {
        #     'pk' : new_question.pk,
        #     'fields' : {
        #         'username' : new_question.user.username,
        #         'title' : new_question.title,
        #         'question' : new_question.question,
        #         'date' : new_question.date,
        #         'book' : new_question.book.title,
        #         'book_id' : new_question.book,
        #     }
        # }
        new_comment.save()
        # return JsonResponse(result)
    return HttpResponseNotFound()

@login_required(login_url='/login/')
@csrf_exempt
def create_response(request, pk):
    discussion_head = Discussion.objects.get(pk = pk)
    if request.method == 'POST':
        user = request.user
        # user = USER_BARU
        date = datetime.now()
        response = request.POST.get('response')
        new_response = Response(user = user, response_to = discussion_head, date = date, response = response)
        result = {
            'pk' : new_response.pk,
            'fields' : {
                'username' : new_response.user.username,
                'comment' : new_response.response,
                'date' : new_response.date
            }
        }
        new_response.save()
        return JsonResponse(result)
    return HttpResponseNotFound()

@login_required(login_url='/login/')
@csrf_exempt
def delete_comment(request, username, id):
    if request.method == 'DELETE' and request.user.username == username:
        comment = Discussion.objects.get(pk = id)
        comment.delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

@login_required(login_url='/login/')
@csrf_exempt
def delete_response(request, username, id):
    if request.method == 'DELETE' and request.user.username == username:
        response = Response.objects.get(pk = id)
        response.delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

def show_discussion_json_2(request):
    data = Discussion.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_discussion_json(request):
    models = Discussion.objects.all()
    serialized_data = []
    for model in models:
        connected_comments = Response.objects.filter(response_to = model)
        comment_counts = len(connected_comments)
        product = model.product
        user = model.user
        model_data = {
            "model": "discussion.discussion",
            "pk": model.pk,  # Include the "pk" field
            "fields": {
                "product": product.name,
                "product_id" : str(product.id),
                "user": user.username,
                "date": str(model.date),  # Convert the date to a string
                "topic": model.topic,
                "comment": model.comment,
                "comment_counts" : comment_counts,
                'owned_by_current_user': user.username == request.user.username,
            }
        }
        serialized_data.append(model_data)
        # abis udah append ke serialized_data
    json_data = json.dumps(serialized_data)
    return HttpResponse(json_data, content_type="application/json")

def show_response_json(request):
    data = Response.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_uniqueresponse_json(request, id):
    comment = get_object_or_404(Discussion, pk=id)
    response = Response.objects.filter(response_to=comment)

    serialized_data = []
    for model in response:
        user = model.user
        model_data = {
            "model": "discussion.response",
            "pk": model.pk,  # Include the "pk" field
            "fields": {
                "user": user.username,
                "reponse_to": model.response_to.pk,
                "date": str(model.date),  # Convert the date to a string
                "response" :  model.response,
                'owned_by_current_user': user.username == request.user.username,
            }
        }
        serialized_data.append(model_data)
        # abis udah append ke serialized_data
    json_data = json.dumps(serialized_data)
    return HttpResponse(json_data, content_type="application/json")

def show_product_json(request):
    product = Product.objects.all()
    return HttpResponse(serializers.serialize('json', product), content_type="application/json")
    
def product_details(request, id):
    product = Product.objects.filter(pk = id)
    return HttpResponse(serializers.serialize('json', product), content_type="application/json")

@login_required(login_url='/login/')
def show_response(request, id_head):
    comment = Discussion.objects.get(pk = id_head)
    response = Response.objects.filter(response_to=comment)
    context = {
        'name' : request.user,
        'comment': comment,
        'response': response,
    }
    
    return render(request, "discussion/response.html", context)