from django.urls import path
from . import views
from .views import article_list, delete_article, edit_article, create_article_ajax, get_articles

app_name = 'blog'

urlpatterns = [
    path('blog/', article_list, name='article_list'),
    path('blog/my_articles/', views.my_articles, name='my_articles'),
    path('blog/edit-article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('blog/delete/<int:article_id>/', delete_article, name='delete_article'),
    path('blog/create/ajax/', create_article_ajax, name='create_article_ajax'),
    path('blog/json/', views.show_json, name='show_json'),
    path('blog/xml/', views.show_xml, name='show_xml'),
    path('blog/view/<int:article_id>/', views.view_article, name='view_article'),
    path('blog/get-articles/', get_articles, name='get_articles'),
    path('get-json/', views.get_json, name='get_json'),
]
