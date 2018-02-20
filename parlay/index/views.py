from django.shortcuts import render,redirect, get_object_or_404
from .models import Book, Wager
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q


from .forms import SignUpForm, ProfileForm, WagerForm

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
                                              'user': username
                                              })


def bdetail(request,book_id):
    book = Book.objects.get(pk=book_id)

    return render(request, 'par/detail.html', {'book': book,})

def profile(request, user_id):
    username = None
    if request.user.is_authenticated:
        profile_user = User.objects.get(pk=user_id)
    return render(request, 'par/profile.html', {'username': profile_user})


@login_required
def add_book(request, book_id):
    user = request.user
    if Book.objects.get(pk = book_id) in user.profile.books_read.all():
        pass
    else:
        user.profile.books_read.add(Book.objects.get(pk = book_id))
        user.profile.save()

    # return redirect('detail-book', Book.objects.get(pk = book_id))
    return HttpResponseRedirect(reverse('detail-book', args=(book_id,)))


@login_required
def add_friend(request,user_id):
    host = request.user
    if User.objects.get(pk = user_id) in host.profile.friends.all():
        pass
    else:
        host.profile.friends.add(User.objects.get(pk = user_id))
        host.profile.save()
        User.objects.get(pk = user_id).profile.friends.add(host)
        User.objects.get(pk = user_id).save()
    profile_user = User.objects.get(pk=user_id)
    # return redirect('profile', user_id = profile_user.pk )
    return HttpResponseRedirect(reverse('profile', args=(user_id,)))

@login_required
def remove_friend(request,user_id):
    host = request.user
    request.user.profile.friends.remove(User.objects.get(pk=user_id))
    # host.profile.save()
    User.objects.get(pk=user_id).profile.friends.remove(request.user)
    # User.objects.get(pk=user_id).save()

    # return redirect('profile', user_id = profile_user.pk )
    return HttpResponseRedirect(reverse('profile', args=(user_id,)))


@login_required
def edit_profile(request,user_id):
    user = User.objects.get(pk = user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user.profile = form.save(commit=False)
            user.profile.save()
            return redirect('profile', user_id = user.pk )
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'par/edit_profile.html', {'form' : form})


@login_required
def add_wager(request):
    sender = request.user
    if request.method == "POST":
        form = WagerForm(request.POST)
        if form.is_valid():
            Wager = form.save(commit=False)
            Wager.sender = sender
            Wager.save()
            return redirect('wagers')
    else:
        form = WagerForm()
    return render(request, 'par/add_wager.html', {'form': form})


def wagers(request):
    user = request.user
    wagers = Wager.objects.filter (Q(to=user) | Q(sender=user))
    return render(request, 'par/wager-list.html', {'wagers': wagers})


def accept_wager(request, wager_id):
    Wager.objects.get(pk=wager_id).status = str('true')
    Wager.objects.get(pk=wager_id).save()
    return redirect('wagers')


def decline_wager(request, wager_id):
    Wager.objects.get(pk=wager_id).status = str('false')
    Wager.objects.get(pk=wager_id).save()
    return redirect('wagers')