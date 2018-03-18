from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Wager, Book, WagerQuestion
from django.forms.formsets import BaseFormSet


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'favourite_genres', 'favourite_authors',
                  'favourite_books', )
        labels = {
            'favourite_genres': 'Любимые жанры',
            'favourite_authors': 'Любимые авторы',
            'favourite_books': 'Любимые книги',
        }
        widgets = {
            'bio': forms.Textarea(),
            'favourite_genres': forms.Textarea(),
            'favourite_authors': forms.Textarea(),
            'favourite_books': forms.Textarea(),
        }


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
            'to': 'Кому',
            'book': 'Книга',
            'bet': 'Ставка',
            'duration': 'Длительность',
        }
        widgets = {
            'bet': forms.TextInput()
        }


class WagerEditForm(forms.ModelForm):
    class Meta:
        model = Wager
        fields = ('new_bet', 'new_duration')
        labels = {
            'new_bet': 'Измените ставку',
            'new_duration': 'Измените длительность',
        }
        widgets = {
            'new_bet': forms.TextInput()
        }


class WagerQuestionForm(forms.ModelForm):
    class Meta:
        model = WagerQuestion
        fields = {'question'}
        labels = {
            'question': 'Напишите вопрос по теме книги',
        }


class WagerAnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Calling next() on the iterator/generator here:
        try:
            list_item = kwargs.pop('item_iterator').__next__()
        except StopIteration:
            list_item='1'
        super(WagerAnswerForm, self).__init__(*args, **kwargs)

        # Now you can assign whatever you passed in to an attribute
        # on one of the form elements.
        self.fields['answer'].label = list_item
    class Meta:
        model = WagerQuestion
        fields = {'answer'}
        labels = {
            'answer': 'Напишите ответ на данный вопрос',
        }
