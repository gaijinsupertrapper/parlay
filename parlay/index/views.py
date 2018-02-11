from django.shortcuts import render,redirect
from .models import Book
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'par/signup.html', {'form': form})


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
    return render(request, 'par/index.html', {'books': Book.objects.all,
                                              'user': username})


def bdetail(request,book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'par/detail.html', {'book': book})