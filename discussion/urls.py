from django.urls import path
from discussion.views import *

app_name = 'discussion'

urlpatterns = [
    path('', show_discussion, name='show_discussion' ),
]