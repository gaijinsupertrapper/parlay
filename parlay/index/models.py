from django.db import models
from django.db.models import TextField
from django.forms import ModelForm
from django.contrib.auth.forms import User
from .forms import SignUpForm

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.IntegerField(default=100)


class Book(models.Model):
    title = models.CharField(max_length = 150, default = r'Yet another book')
    author = models.CharField(max_length = 100, default = r'By yet another author')
    release = models.DateField()
    description = models.CharField(max_length = 500, default = r'Description for the book')
    def __str__(self):
        return self.title
