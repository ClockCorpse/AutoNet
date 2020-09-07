from django.contrib.auth.models import User
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    profilePassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile