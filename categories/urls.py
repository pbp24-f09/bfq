from django.urls import path
from categories.views import show_categories, add_product_ajax

app_name = 'categories'

urlpatterns = [
    path('', show_categories, name='show_categories'),
    path('add-product-ajax', add_product_ajax, name='add_product_ajax'),
]