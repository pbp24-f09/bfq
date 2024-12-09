from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('main/', views.customer_dashboard, name='customer_dashboard'),
    path('categories/', views.customer_categories, name='customer_categories'),
    path('blog/', views.customer_blog, name='customer_blog'),    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-photo/', views.update_photo, name='update_photo'),
    path('delete-photo/', views.delete_photo, name='delete_photo'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('login-flutter/', views.login_flutter, name='login_flutter'),
    path('register-flutter/', views.register_flutter, name='register_flutter'),
    path('logout-flutter/', views.logout_flutter, name='logout_flutter'),
    path('profile-flutter/', views.profile_flutter, name='profile_flutter'),
    path('update-profile-flutter/', views.update_profile_flutter, name='update_profile_flutter'),
    path('update-photo-flutter/', views.update_photo_flutter, name='update_photo_flutter'),
    path('delete-photo-flutter/', views.delete_photo_flutter, name='delete_photo_flutter'),
    path('change-password-flutter/', views.change_password_flutter, name='change_password_flutter'),
    path('delete-account-flutter/', views.delete_account_flutter, name='delete_account_flutter'),
]
