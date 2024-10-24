import datetime
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, EditPhotoForm
from .decorators import role_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Set cookie untuk 'last_login'
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))

            # Redirect ke dashboard sesuai role
            if user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')

        else:
            # Tambahkan pesan error jika login gagal
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            data = f"success,{user.full_name},{user.email},{user.age},{user.gender},{user.phone_number}"
            return HttpResponse(data, content_type='text/plain')
        else:
            errors = []
            for field, messages in form.errors.items():
                for message in messages:
                    errors.append(f"{field}:{message}")
            return HttpResponse("error," + ",".join(errors), content_type='text/plain', status=400)
    return HttpResponse("Method not allowed", status=405)

@login_required
@csrf_exempt
def update_photo(request):
    if request.method == 'POST':
        user = request.user
        new_photo_url = request.POST.get('profile_photo', '')

        # Periksa apakah URL valid (tidak kosong)
        if new_photo_url.strip():
            user.profile_photo = new_photo_url
            user.save()  # Simpan perubahan ke database
            return HttpResponse(f"success,{new_photo_url}", content_type='text/plain')
        else:
            return HttpResponse("error:Invalid URL", content_type='text/plain', status=400)
    return HttpResponse("Method not allowed", status=405)

@login_required
@csrf_exempt
def delete_photo(request):
    if request.method == 'POST':
        user = request.user
        user.profile_photo = None
        user.save()
        return HttpResponse("Photo deleted", content_type='text/plain')
    return HttpResponse("Method not allowed", status=405)

@login_required
@role_required('customer')
def customer_dashboard(request):
    return render(request, 'main_customer.html')

@login_required
@role_required('admin')
def admin_dashboard(request):
    return render(request, 'main_admin.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})


def logout_user(request):
    logout(request)
    response = redirect('main:show_main')
    response.delete_cookie('last_login')
    return response