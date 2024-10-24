from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-photo/', views.update_photo, name='update_photo'),
    path('delete-photo/', views.delete_photo, name='delete_photo'),
    # path('change-password/', views.change_password, name='change_password'),
]