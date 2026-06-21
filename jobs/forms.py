from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('skills', 'preferred_roles', 'preferred_locations', 'experience_years')
        widgets = {
            'skills': forms.TextInput(attrs={
                'placeholder': 'e.g. Python, Django, Machine Learning, SQL',
                'class': 'form-control',
            }),
            'preferred_roles': forms.TextInput(attrs={
                'placeholder': 'e.g. Backend Developer, Data Scientist',
                'class': 'form-control',
            }),
            'preferred_locations': forms.TextInput(attrs={
                'placeholder': 'e.g. Remote, New York (leave blank for any)',
                'class': 'form-control',
            }),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'skills': 'Your Skills',
            'preferred_roles': 'Preferred Job Roles',
            'preferred_locations': 'Preferred Locations',
            'experience_years': 'Years of Experience',
        }
