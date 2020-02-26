from django import forms
from django.contrib.auth.models import User
from fantasy.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AddStatForm(forms.Form):
    match_id = forms.CharField(label='Match id', max_length=10)
