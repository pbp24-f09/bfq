from django.urls import path
from categories.views import (
    show_categories, show_categories_admin, add_product_ajax_cat, edit_product_cat, delete_product_cat,
    search_filter
    )

app_name = 'categories'

urlpatterns = [
    path('categories/', show_categories, name='show_categories'),
    path('admin-categories/', show_categories_admin, name='show_categories_admin'),
    path('add-product-ajax-cat', add_product_ajax_cat, name='add_product_ajax_cat'),
    path('edit-product-cat/<uuid:id>', edit_product_cat, name='edit_product_cat'),
    path('delete-product-cat/<uuid:id>', delete_product_cat, name='delete_product_cat'),
    path('search-filter/', search_filter, name='search_filter'),
]