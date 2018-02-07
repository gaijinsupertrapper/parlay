from django.db import models
from django.db.models import TextField
from django.forms import ModelForm

class Book(models.Model):
    title = models.CharField(max_length = 150, default = r'Yet another book')
    author = models.CharField(max_length = 100, default = r'By yet another author')
    release = models.DateField()
    description = models.CharField(max_length = 500, default = r'Description for the book')
    def __str__(self):
        return self.title
