from django.urls import path
from . import views
from .views import article_list, delete_article, edit_article, create_article_ajax, get_articles

app_name = 'blog'

urlpatterns = [
    path('', article_list, name='article_list'),
    path('my_articles/', views.my_articles, name='my_articles'),
    path('edit-article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:article_id>/', delete_article, name='delete_article'),
    path('create/ajax/', create_article_ajax, name='create_article_ajax'),
    path('json/', views.show_json, name='show_json'),
    path('xml/', views.show_xml, name='show_xml'),
    path('view/<int:article_id>/', views.view_article, name='view_article'),
    path('get-articles/', get_articles, name='get_articles'),  # Endpoint baru
    
]