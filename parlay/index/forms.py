from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    bio = forms.CharField(max_length=250, initial="Your bio here")
    tokens = forms.IntegerField(initial=100, disabled = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'tokens', 'password1', 'password2', )

class Profile():
    pass