from django.shortcuts import render,redirect, get_object_or_404
from .models import Book, Wager
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from requests_html import session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

from .forms import SignUpForm, ProfileForm, WagerForm, BookUrlForm

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
    books_list = Book.objects.all()
    paginate = Paginator(books_list,9)
    page = request.GET.get('page')
    books = paginate.get_page(page)
    return render(request, 'par/index.html', {'books': books,
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
            Wager.duration = form.cleaned_data['duration']*86400
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
    wager = Wager.objects.get(pk=wager_id)
    wager.status = 'true'
    wager.save()
    return redirect('wagers')


def decline_wager(request, wager_id):
    wager = Wager.objects.get(pk=wager_id)
    wager.status = 'false'
    wager.save()
    return redirect('wagers')


def end_wager(request, wager_id):
    Wager.objects.get(pk=wager_id).delete()

    return redirect('wagers')


def friends_list(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'par/friends.html', {'username': user})


def books_list(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'par/books.html', {'username': user})


def search(request):
    if request.method == "GET":
        q = request.GET.get('q')
        if q:
            return redirect('search-results', search_query=q)
        else:
            return redirect('index')
    else:
        return redirect('profile')


def search_results(request, search_query):
    users = User.objects.filter(username__icontains = search_query)[:5]
    books = Book.objects.filter(title__icontains = search_query)[:5]
    return render(request, 'par/search-results.html', {'users': users,
                                              'books': books,
                                            'q': search_query})


def create_book(request):
    if request.method == "POST":
        form = BookUrlForm(request.POST)
        if form.is_valid():

            r = session.get(form.cleaned_data['url'])
            title = r.html.find('.biblio_book_name', first=True).text
            author = r.html.find('.biblio_book_author__link', first=True).text
            description_list = r.html.find('.biblio_book_descr_publishers p')
            description = str()

            for i in range(len(description_list)):
                description += description_list[i].text
                description += '\n'

            book = Book.objects.create( title=title, author=author, description=description , url=form.cleaned_data['url'])
            return redirect('index')
    else:
        form = BookUrlForm()
    return render(request, 'par/add-book.html', {'form': form})