  # -*- coding: utf-8 -*-
__author__ = 'zisakadze'

from django import forms
from skipass.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text='შეიყვანეთ პაროლი')
    email = forms.CharField(help_text="შეიყვანეთ თქვენი e-mail")
    username = forms.CharField(help_text="შეიყვანეთ მომხმარებლის სახელი")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    card_number = forms.IntegerField(help_text='შეიყვანეთ თქვენი ბარათის ნომერი', required=True)
    class Meta:
        model = UserProfile
        fields = ('card_number',)