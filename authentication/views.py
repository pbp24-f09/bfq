import datetime
from .forms import UserRegistrationForm, EditProfileForm
from .decorators import role_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

import json
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout
from django.utils.dateformat import format
from django.utils.timezone import localtime
from django.contrib import messages
from .forms import UserLoginForm
import datetime

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
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Set cookie untuk 'last_login'
            response = redirect('main:show_main')
            response.set_cookie('last_login', str(datetime.datetime.now()))

            # Redirect ke dashboard sesuai role
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')  # Admin Dashboard
            else:
                return redirect('customer_dashboard')  # Customer Dashboard

        else:
            # Jika login gagal
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

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
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Verifikasi password lama
        if not check_password(old_password, user.password):
            messages.error(request, 'Incorrect current password.', extra_tags='error')
            return redirect('change_password')

        # Validasi password baru
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.', extra_tags='error')
            return redirect('change_password')

        # Ubah password dan update session
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully!', extra_tags='success')
        return redirect('change_password')
    
    return render(request, 'change_password.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'})

        user = authenticate(username=username, password=password)
        if user is not None and user == request.user:
            user.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
@role_required('customer')
def customer_dashboard(request):
    return render(request, 'main_customer.html')

@login_required
@role_required('customer')
def customer_categories(request):
    return render(request, 'categories.html')

@login_required
@role_required('admin')
def admin_categories(request):
    return render(request, 'categories_admin.html')

@login_required
def customer_blog(request):
    return render(request, 'blog/article_list.html')

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


####### API views for Flutter ###########
@csrf_exempt
def login_flutter(request):
    if request.method == 'POST':
        # Ambil data dari request body (gunakan JSON jika diperlukan)
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return JsonResponse({
                "status": False,
                "message": "Invalid request. Missing username or password."
            }, status=400)

        # Autentikasi pengguna
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # Role pengguna (ubah sesuai atribut role di model Anda)
                role = "admin" if user.is_staff else "customer"

                # Respons sukses
                return JsonResponse({
                    "username": user.username,
                    "role": role,  # Sertakan role pengguna
                    "full_name": user.full_name,
                    "profile_photo": user.profile_photo if user.profile_photo else None,
                    "status": True,
                    "message": "Login sukses!"
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Login gagal, akun dinonaktifkan."
                }, status=401)

        # Jika autentikasi gagal
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserRegistrationForm(data)
            if form.is_valid():
                user = form.save()
                return JsonResponse({
                    "status": "success",
                    "message": "User registered successfully!",
                    "username": user.username
                }, status=200)
            else:
                return JsonResponse({
                    "status": "error",
                    "errors": form.errors
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON input."
            }, status=400)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Only POST method is allowed."
        }, status=405)
    

@csrf_exempt
def logout_flutter(request):
    username = request.user.username

    try:
        auth_logout(request)
        user = None
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@login_required
@csrf_exempt
def profile_flutter(request):
    user = request.user
    profile_photo = user.profile_photo  # Ambil langsung nilai string profile_photo

    # Jika profile_photo bukan URL absolut, tambahkan prefix host jika diperlukan
    if profile_photo and not profile_photo.startswith("http"):
        profile_photo = request.build_absolute_uri(profile_photo)

    profile_data = {
        "id": user.id,
        "username": user.username,
        "full_name": getattr(user, 'full_name', None),
        "email": user.email,
        "date_joined": format(localtime(user.date_joined), 'F j, Y'),
        "age": getattr(user, 'age', None),
        "gender": getattr(user, 'gender', None),
        "phone_number": getattr(user, 'phone_number', None),
        "profile_photo": profile_photo,  # Gunakan nilai yang sudah diproses
        "role": "admin" if user.is_staff else "customer",
        "is_admin": user.is_staff or user.is_superuser,
    }
    return JsonResponse(profile_data, safe=False)

@csrf_exempt
@login_required
def update_profile_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        # Update fields if present
        user.full_name = data.get('full_name', user.full_name)
        user.email = data.get('email', user.email)
        user.age = data.get('age', getattr(user, 'age', None))
        user.gender = data.get('gender', getattr(user, 'gender', None))
        user.phone_number = data.get('phone_number', getattr(user, 'phone_number', None))
        user.save()

        # Respond with updated profile
        return JsonResponse({
            "status": "success",
            "message": "Profile updated successfully!",
        })
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)


from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

@login_required
@csrf_exempt
def update_photo_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Membaca JSON dari request.body
            photo_url = data.get('photo_url', '')

            if not photo_url.strip():
                return JsonResponse({"status": "error", "message": "Photo URL is required"}, status=400)

            user = request.user
            user.profile_photo = photo_url
            user.save()
            return JsonResponse({"status": "success", "message": "Photo updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


@login_required
@csrf_exempt
def delete_photo_flutter(request):
    if request.method == 'POST':
        user = request.user
        user.profile_photo = None
        user.save()  # Simpan perubahan ke database
        return JsonResponse({
            "status": "success",
            "message": "Photo deleted successfully"
        })
    return JsonResponse({
        "status": "error",
        "message": "Method not allowed"
    }, status=405)

@login_required
@csrf_exempt
def delete_account_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        username = data.get('username', '')
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')

        # Verifikasi password
        if password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'}) 
        
        user = authenticate(username=username, password=password)
        if user is not None and user == request.user:
            user.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
@csrf_exempt
def change_password_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Expecting JSON request
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            user = request.user

            # Verify old password
            if not check_password(old_password, user.password):
                return JsonResponse(
                    {"status": "error", "message": "Incorrect current password."},
                    status=400
                )

            # Validate new password
            if new_password != confirm_password:
                return JsonResponse(
                    {"status": "error", "message": "New passwords do not match."},
                    status=400
                )

            # Change password and update session
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            return JsonResponse(
                {"status": "success", "message": "Password changed successfully!"},
                status=200
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid request format."}, status=400
            )
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
