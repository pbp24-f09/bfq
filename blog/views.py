from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from .models import Article
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

@csrf_exempt
def create_article_ajax(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        topic = request.POST.get('topic')
        content = request.POST.get('content')
        
        # Buat artikel baru
        new_article = Article.objects.create(
            title=title,
            topic=topic,
            content=content,
            author=request.user if request.user.is_authenticated else None
        )
        
        # Kirim respons JSON
        return JsonResponse({
            'id': new_article.id,
            'title': new_article.title,
            'author': new_article.author.username if new_article.author else 'Anonymous',
            'content': new_article.content,
        })

def article_list(request):
    # Fungsi untuk menampilkan semua artikel
    articles = Article.objects.all()
    return render(request, 'blog/article_list.html', {'articles': articles})

def my_articles(request):
    # Fungsi untuk menampilkan artikel milik user yang login
    if request.user.is_authenticated:
        articles = Article.objects.filter(author=request.user)
    else:
        articles = []  # Jika user tidak login, tampilkan daftar kosong
    return render(request, 'blog/my_articles.html', {'articles': articles})

def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blog:article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/edit_article.html', {'form': form, 'article': article})

def delete_article(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        return JsonResponse({'message': 'Article deleted successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def show_json(request):
    articles = Article.objects.all().values('id', 'title', 'author', 'content')
    return JsonResponse(list(articles), safe=False)

def show_xml(request):
    articles = Article.objects.all()
    root = ET.Element("articles")

    for article in articles:
        article_element = ET.SubElement(root, "article")
        ET.SubElement(article_element, "id").text = str(article.id)
        ET.SubElement(article_element, "title").text = article.title
        ET.SubElement(article_element, "author").text = article.author.username if article.author else 'Anonymous'
        ET.SubElement(article_element, "content").text = article.content

    response = HttpResponse(ET.tostring(root), content_type='application/xml')
    return response

