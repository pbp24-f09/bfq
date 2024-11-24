# forms.py di app authentication
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'age', 'gender', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")  # Tambahkan error ke field confirm_password
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        # Hanya untuk registrasi customer (bukan admin)
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'age', 'gender', 'phone_number']

class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)