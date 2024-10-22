from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm

def create_article(request):
    # Fungsi untuk membuat artikel baru
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            # Menentukan author jika user login, jika tidak biarkan None
            article.author = request.user if request.user.is_authenticated else None
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/create_article.html', {'form': form})

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

def edit_article(request, pk):
    # Fungsi untuk mengedit artikel yang ada
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/edit_article.html', {'form': form})

def delete_article(request, pk):
    # Fungsi untuk menghapus artikel
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')
    return render(request, 'blog/delete_article.html', {'article': article})
