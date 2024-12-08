import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Article
from .forms import ArticleForm
import xml.etree.ElementTree as ET
from django.template.loader import render_to_string
from .models import Article
from django.views.decorators.csrf import csrf_exempt


@csrf_protect
@login_required
@require_POST
def create_article_ajax(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        topic = request.POST.get('topic')
        content = request.POST.get('content')
        author = request.user  # Asumsi pengguna yang diautentikasi adalah penulis

        # Validasi input (opsional namun direkomendasikan)
        if not title or not content:
            return JsonResponse({'success': False, 'error': 'Title and content are required.'}, status=400)

        # Buat artikel baru
        article = Article.objects.create(title=title, topic=topic, content=content, author=author)

        # Render HTML untuk artikel baru menggunakan template partial
        article_html = render_to_string('blog/article_card.html', {'article': article, 'request': request}, request=request)

        return JsonResponse({'success': True, 'html': article_html})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/article_list.html', {'articles': articles})



@login_required
def my_articles(request):
    # Fungsi untuk menampilkan artikel milik user yang login
    articles = Article.objects.filter(author=request.user)
    return render(request, 'blog/my_articles.html', {'articles': articles})

@login_required
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

@login_required
@require_POST
def delete_article(request, article_id):
    # Fungsi untuk menghapus artikel
    article = get_object_or_404(Article, pk=article_id)

    if article.author != request.user:
        return JsonResponse({'error': 'You are not allowed to delete this article'}, status=403)

    article.delete()
    return JsonResponse({'message': 'Article deleted successfully!'})

@login_required
def show_json(request):
    articles = Article.objects.filter(author=request.user).values('id', 'title', 'author__username', 'content')
    return JsonResponse(list(articles), safe=False)

@login_required
def get_json(request):
    articles = list(Article.objects.values())  # Mengambil data dari model Article
    return JsonResponse({'articles': articles})

@login_required
def show_xml(request):
    # Fungsi untuk menampilkan semua artikel dalam format XML
    articles = Article.objects.filter(author=request.user)
    root = ET.Element("articles")

    for article in articles:
        article_element = ET.SubElement(root, "article")
        ET.SubElement(article_element, "id").text = str(article.id)
        ET.SubElement(article_element, "title").text = article.title
        ET.SubElement(article_element, "author").text = article.author.username if article.author else 'Anonymous'
        ET.SubElement(article_element, "content").text = article.content

    response = HttpResponse(ET.tostring(root), content_type='application/xml')
    return response

@login_required
def view_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'blog/view_article.html', {'article': article})

@login_required
@login_required
def get_articles(request):
    articles = Article.objects.all()
    articles_data = []
    for article in articles:
        is_author = article.author == request.user
        articles_data.append({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author.username,
            'is_author': is_author,
            'time': article.created_at,
            'topic': article.topic
        })

    return JsonResponse({'articles': articles_data})


def blog_home(request):
    articles = Article.objects.all()
    return render(request, 'blog/home.html', {'articles': articles})


@csrf_exempt
def delete_article_flutter(request, article_id):
    if request.method == 'POST':
        try:
            # Retrieve the article by ID
            article = Article.objects.get(id=article_id)
            # Perform the delete operation
            article.delete()
            # Return success response
            return JsonResponse({'success': True, 'message': 'Article deleted successfully'})
        except Article.DoesNotExist:
            # If the article does not exist
            return JsonResponse({'success': False, 'message': 'Article not found'}, status=404)
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        # If the request is not POST
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt  
def create_article_flutter(request):
    if request.method == 'POST':
        # Parse the JSON body
        data = json.loads(request.body)
        new_article = Article.objects.create(
            title = data['title'],
            topic = data['topic'],
            content = data['content'],
            author = request.user
        )
        new_article.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_article_flutter(request, article_id):
    try:
        # Retrieve the article by ID
        article = Article.objects.get(id=article_id)

        # Check if the article's author matches the current user
        if article.author != request.user:
            return JsonResponse({'success': False, 'message': 'You are not authorized to edit this article'}, status=403)

        # Ensure the request is a POST request
        if request.method == 'POST':
            # Parse JSON body
            data = json.loads(request.body)
            title = data.get('title')
            topic = data.get('topic')
            content = data.get('content')

            # Validate the required fields
            if not title or not content:
                return JsonResponse({'success': False, 'message': 'Title and content are required'}, status=400)

            # Update the article
            article.title = title
            article.topic = topic
            article.content = content
            article.save()
            return JsonResponse({'success': True, 'message': 'Article updated successfully'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    except Article.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Article not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
