from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Wager, Book


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', )


class BookUrlForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('url',)

class WagerForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(WagerForm, self).__init__(*args, **kwargs)
        self.fields['to'].queryset = User.objects.get(username=user).profile.friends.all()
        self.fields['book'].queryset = User.objects.get(username=user).profile.books_read.all()

    class Meta:
        model = Wager
        fields=('to','book','bet', 'duration')
        labels = {
            'to': 'Choose a user',
            'book': 'Select a book',
            'bet': 'Place a bet',
            'duration': 'Select a duration of this wager in days',
        }
        widgets = {
            'bet': forms.TextInput()
        }

