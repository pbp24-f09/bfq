from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Article
from .forms import ArticleForm
import xml.etree.ElementTree as ET

@csrf_exempt
@login_required
def create_article_ajax(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        topic = request.POST.get('topic')
        content = request.POST.get('content')

        if not title or not topic or not content:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            # Buat artikel baru dengan waktu otomatis terisi di 'created_at'
            new_article = Article.objects.create(
                title=title,
                topic=topic,
                content=content,
                author=request.user
            )
            
            return JsonResponse({
                'id': new_article.id,
                'title': new_article.title,
                'author': new_article.author.username,
                'content': new_article.content,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

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
    # Fungsi untuk mengedit artikel
    article = get_object_or_404(Article, pk=article_id)

    if article.author != request.user:
        return JsonResponse({'error': 'You are not allowed to edit this article'}, status=403)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blog:article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/edit_article.html', {'form': form, 'article': article})

@require_POST
def delete_article(request, article_id):
    # Fungsi untuk menghapus artikel
    article = get_object_or_404(Article, pk=article_id)

    if article.author != request.user:
        return JsonResponse({'error': 'You are not allowed to delete this article'}, status=403)

    article.delete()
    return JsonResponse({'message': 'Article deleted successfully!'})

def show_json(request):
    # Fungsi untuk menampilkan semua artikel dalam format JSON
    articles = Article.objects.all().values('id', 'title', 'author__username', 'content')
    return JsonResponse(list(articles), safe=False)

def show_xml(request):
    # Fungsi untuk menampilkan semua artikel dalam format XML
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
