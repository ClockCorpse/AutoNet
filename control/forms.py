from django.contrib.auth.models import User
from django import forms
from .models import Profile, ExtendedUser, UserConfig, ROCommunityString, RWCommunityString


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserConfigForm(forms.ModelForm):
    class Meta:
        model = UserConfig
        fields = ['configPath']


class UserExtendedForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ['configLocation']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profileName', 'profilePassword', 'profileEnablePassword']


class ROCommunityStringForm(forms.ModelForm):
    class Meta:
        model = ROCommunityString
        fields = ['name', 'communityString']


class RWCommunityStringForm(forms.ModelForm):
    class Meta:
        model = RWCommunityString
        fields = ['name', 'communityString']
