from django.contrib.auth.models import User
from django import forms
from .models import CattleImage

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CattleImageForm(forms.ModelForm):

    class Meta:
        model = CattleImage
        fields = ['classify_img']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']