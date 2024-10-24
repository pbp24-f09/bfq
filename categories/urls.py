from django.urls import path
from categories.views import show_categories

app_name = 'categories'

urlpatterns = [
    path('', show_categories, name='show_categories'),
]