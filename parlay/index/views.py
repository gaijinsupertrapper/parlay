from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import Book

def index(request):
    return render(request, 'par/index.html', {'books': Book.objects.all})

def bdetail(request,book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'par/detail.html', {'book': book})