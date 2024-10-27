from django.urls import path
from discussion.views import *

app_name = 'discussion'

urlpatterns = [
    path('discussion/', show_discussion, name='show_discussion' ),
    path('create_comment/', create_comment, name='create_comment'),
    path('create_response/<int:pk>', create_response, name="create_response"),
    path('delete_comment/<str:username>/<int:id>', delete_comment, name="delete_comment"),
    path('delete_response/<str:username>/<uuid:id>', delete_response, name="delete_response"),
    path('uniqueresponse/json/<int:id>', show_uniqueresponse_json, name="show_uniqueresponse_json"),
    path('show_product_json/json/', show_product_json, name="show_product_json"),
    path('discussion/json2/', show_discussion_json_2, name="show_discussion_json_2"),
    path('show_response/<int:id_head>/', show_response, name="show_response"),
    path('discussion/json/', show_discussion_json, name="show_discussion_json"),
    path('comment/json/', show_response_json, name="show_response_json"),
    path('product_details/json/<int:id>', product_details, name="product_details"),
]