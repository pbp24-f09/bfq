from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main.views import (
    show_main, show_main_admin, create_product, show_xml, show_json, show_xml_by_id, 
    show_json_by_id, edit_product, delete_product, add_product_ajax, product_list, create_product_flutter,
    edit_product_flutter, product_detail_json, get_product_detail
)

app_name = 'main'

urlpatterns = [
    # Publicly accessible main page
    path('', show_main, name='show_main'),
    path('main_admin', show_main_admin, name='show_main_admin'),
    path('api/products/', product_list, name='product-list'),
    
    # Views requiring authentication
    path('create-product', create_product, name='create_product'),  # Requires login
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),  # Requires login
    path('delete-product/<uuid:id>', delete_product, name='delete_product'),  # Requires login
    path('add-product-ajax', add_product_ajax, name='add_product_ajax'),  # Requires login
    
    # api XML dan JSON
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    
    # flutter features
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
    path('edit-flutter/<uuid:id>', edit_product_flutter, name='edit_product_flutter'),
    path('product-json/<str:id>/', product_detail_json, name='product_detail_json'),
    path('get-product/<str:id>', get_product_detail, name='get_product_detail'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
