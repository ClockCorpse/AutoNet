from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profileName','profilePassword','profileEnablePassword']

# class ChangePasswordForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['password','newPassword']
#         widgets = {'newPassword':forms.PasswordInput}