from django.shortcuts import render,redirect, get_object_or_404
from .models import Book, Wager, WagerQuestion
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from requests_html import HTMLSession
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.forms import formset_factory
from django.utils.functional import curry
import cloudinary
import cloudinary.uploader
import cloudinary.api
import pytz

from .forms import SignUpForm,\
    ProfileForm, WagerForm,\
    WagerEditForm, BookUrlForm,\
    WagerQuestionForm,\
    WagerAnswerForm, \
    WagerCheckForm


def check_new_wagers(user):
    received_wagers = Wager.objects.filter(to=user)
    unchecked = int()
    for wager in received_wagers:
        if (wager.status == 'none'):
            unchecked += 1
    return unchecked

cloudinary.config(
  cloud_name = "parlay",
  api_key = "426334496788595",
  api_secret = "JDuFH0AnBrGMSmJGVb5ARFue1mQ")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile', user_id=user.id)
    else:
        form = SignUpForm()
    return render(request, 'par/signup.html', {'form': form})


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
        user = request.user
        new = check_new_wagers(user)
        books_list = Book.objects.order_by('-read_by', 'title')
        paginate = Paginator(books_list, 9)
        page = request.GET.get('page')
        books = paginate.get_page(page)

        return render(request, 'par/index.html', {'books': books,
                                                  'user': username, 'new': new
                                                  })
    else:
        return render(request, 'par/landing.html')



def bdetail(request,book_id):
    book = Book.objects.get(pk=book_id)
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/detail.html', {'book': book, 'new':new,})

def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/profile.html', {'username': profile_user, 'user': user, 'new':new,})


@login_required
def add_book(request, book_id):
    user = request.user
    if Book.objects.get(pk = book_id) in user.profile.books_read.all():
        pass
    else:
        user.profile.books_read.add(Book.objects.get(pk = book_id))
        user.profile.save()
        book = Book.objects.get(pk=book_id)
        book.read_by +=1
        book.save()

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
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            user.profile = form.save(commit=False)

            user.profile.save()
            return redirect('profile', user_id = user.pk )
    else:
        form = ProfileForm(instance=request.user.profile)
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/edit_profile.html', {'form' : form, 'new': new})


@login_required
def add_wager(request):
    sender = request.user
    too_much = int(0)
    if request.method == "POST":
        form = WagerForm(request.user, request.POST)
        if form.is_valid():
            if form.cleaned_data['bet']>sender.profile.tokens:
                too_much = 1
            elif form.cleaned_data['bet']<=0:
                too_much = 2
            elif form.cleaned_data['duration']<datetime.timedelta(seconds=1):
                too_much = 3
            else:
                Wager = form.save(commit=False)
                Wager.duration = form.cleaned_data['duration']*86400
                Wager.new_duration = Wager.duration
                Wager.new_bet = Wager.bet

                Wager.sender = sender
                Wager.sender_discuss='no'
                Wager.received_discuss='no'
                Wager.save()
                sender.profile.tokens -= Wager.bet
                sender.profile.save()
                return redirect('wagers')
    else:
        form = WagerForm(request.user)
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1

    return render(request, 'par/add_wager.html', {'form': form, 'new': new, 'tm': too_much})


@login_required
def wagers(request):
    today = datetime.datetime.now(tz=pytz.utc)

    user = request.user
    wagers = Wager.objects.filter (Q(to=user) | Q(sender=user)).order_by('until')
    active_wagers=int()
    for wager in wagers:

        if ((wager.sender == user) and (wager.sender_end == 'no')) or ((wager.to == user) and (wager.received_end == 'no')):
            active_wagers+=1


    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/wager-list.html', {'wagers': wagers, 'today': today, 'new': new, 'active': active_wagers,})


@login_required
def edit_wager(request,wager_id):
    wager = Wager.objects.get(pk=wager_id)
    user = request.user
    too_much = int(0)
    if request.method == "POST":
        form = WagerEditForm(request.POST, instance=wager)
        if form.is_valid():
            if (wager.sender == user and wager.sender_discuss == 'true') or (wager.to == user and wager.received_discuss == 'true'):
                return redirect('index')
            else:
                if form.cleaned_data['new_bet']>user.profile.tokens:
                    too_much = 1
                elif form.cleaned_data['new_bet']<=0:
                    too_much = 2
                elif form.cleaned_data['new_duration']<datetime.timedelta(seconds=1):
                    too_much = 3
                else:
                    wager = form.save(commit=False)
                    wager.new_duration = form.cleaned_data['new_duration'] * 86400
                    if wager.sender == user:
                        wager.sender_discuss = 'true'
                        wager.sender_new_bet = form.cleaned_data['new_bet']
                        wager.sender_new_duration = form.cleaned_data['new_duration'] * 86400
                    else:
                        wager.received_discuss = 'true'
                        wager.received_new_bet = form.cleaned_data['new_bet']
                        wager.received_new_duration = form.cleaned_data['new_duration'] * 86400
                    wager.save()
                    return redirect('wagers')
    else:
        form = WagerEditForm()
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new = -1
    return render(request, 'par/edit_wager.html', {'form': form, 'wager': wager, 'tm':too_much, 'new': new})


@login_required
def accept_wager(request, wager_id):
    wager = Wager.objects.get(pk=wager_id)
    wager.status = 'true'
    wager.until = datetime.datetime.now() + wager.new_duration
    wager.save()
    player = wager.to
    sender = wager.sender
    player.profile.tokens -= wager.new_bet
    sender.profile.tokens -= (wager.new_bet - wager.bet)


    player.save()
    sender.save()
    return redirect('wagers')


@login_required
def decline_wager(request, wager_id):
    wager = Wager.objects.get(pk=wager_id)
    wager.status = 'false'
    wager.save()
    return redirect('wagers')


@login_required
def end_wager(request, wager_id):
    wager = Wager.objects.get(pk=wager_id)

    if wager.sender == request.user:
        wager.sender_end = "yes"
        wager.save()
    else:
        wager.received_end = "yes"
        wager.save()

    if (wager.received_end == "yes") and (wager.sender_end == "yes"):
        Wager.objects.get(pk=wager_id).delete()

    return redirect('wagers')


@login_required
def win_wager(request, wager_id):
    wager = Wager.objects.get(pk=wager_id)
    winner = request.user
    if wager.sender == request.user:
        wager.sender_end = "yes"
        wager.save()
        winner.profile.tokens += wager.new_bet*2
        winner.save()
    else:
        wager.received_end = "yes"
        wager.save()
        winner.profile.tokens += wager.new_bet*2
        winner.save()

    if (wager.received_end == "yes") and (wager.sender_end == "yes"):
        Wager.objects.get(pk=wager_id).delete()

    return redirect('wagers')


@login_required
def friends_list(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.user.is_authenticated:
        user_me = request.user
        new = check_new_wagers(user_me)
    else:
        new=-1
    return render(request, 'par/friends.html', {'username': user, 'new': new})


@login_required
def books_list(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.user.is_authenticated:
        user_me = request.user
        new = check_new_wagers(user_me)
    else:
        new=-1
    return render(request, 'par/books.html', {'username': user, 'new':new})


def search(request):
    if request.method == "GET":
        q = request.GET.get('q')
        if q:
            return redirect('search-results', search_query=q)
        else:
            return redirect('index')
    else:
        return redirect('index')


def search_results(request, search_query):
    users = User.objects.filter(username__icontains = search_query)[:5]
    books = Book.objects.filter(Q(title__icontains = search_query) | Q(author__icontains = search_query))[:5]
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/search-results.html', {'users': users,
                                              'books': books,
                                            'q': search_query, 'new':new})


@login_required
def parse_errors(request):
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/parse-error.html', {'new':new})


@login_required
def create_book(request):
    if request.method == "POST":
        form = BookUrlForm(request.POST)
        if form.is_valid():
            url_string = str(form.cleaned_data['url'])
            if url_string.find('litres.ru/')==-1:
                return redirect('parse-errors')
            else:
                url_string='https://'+url_string[url_string.find('litres')::]

                session = HTMLSession()
                r = session.get(url_string)
                if r.html.find('.biblio_book_type', first=True).text == "Аудиокнига":
                    return redirect('parse-errors')
                title = r.html.find('.biblio_book_name', first=True).text
                authors_raw = r.html.find('.biblio_book_author .biblio_book_author__link')
                description_list = r.html.find('.biblio_book_descr_publishers p')
                cover_url = r.html.find('.cover img', first=True).attrs['src']
                description = str()
                authors = str()
                for i in range(len(authors_raw)):
                    authors += authors_raw[i].text
                    authors += ' '
                authors = authors[:-1]
                for i in range(len(description_list)):
                    description += description_list[i].text
                    description += ' \n '
                if Book.objects.filter(url__icontains=form.cleaned_data['url']):
                    return redirect('parse-errors')
                else:
                    book = Book.objects.create( title=title, author=authors, description=description , url=form.cleaned_data['url'],
                                                cover_url=cover_url)
                    adder = request.user
                    adder.profile.books_added += 1
                    adder.profile.tokens += 5
                    adder.save()
                    return redirect('detail-book', book_id=book.id)
    else:
        form = BookUrlForm()
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/add-book.html', {'form': form, 'new': new})


@login_required
def add_questions(request, wager_id):
    user = request.user
    max = Wager.objects.get(pk=wager_id).questions
    WagerQuestionFormSet = formset_factory(WagerQuestionForm,extra=0, min_num=1, max_num=max,validate_max=True)

    if request.method == "POST":
        formset = WagerQuestionFormSet(request.POST)
        if formset.is_valid():

            for form in formset:
                form.save(commit=False)
                if not 'question' in form.cleaned_data:
                    wagerq = WagerQuestion.objects.create(wager=Wager.objects.get(pk=wager_id))
                else:
                    wagerq =  WagerQuestion.objects.create(wager=Wager.objects.get(pk=wager_id),
                                                        question=form.cleaned_data['question'])

            wager = Wager.objects.get(pk=wager_id)
            wager.questions -= int(formset.data['form-TOTAL_FORMS'])
            wager.save()

            return redirect('wagers')

    else:
        formset = WagerQuestionFormSet()
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/add-questions.html', {'formset':formset, 'new': new, 'max':max})


@login_required
def view_questions(request, wager_id):
    questions = WagerQuestion.objects.filter(wager=Wager.objects.get(pk=wager_id))
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new=-1
    return render(request, 'par/questions.html', {'questions': questions, 'new': new})


@login_required
def answer_questions(request,wager_id):

    questions = WagerQuestion.objects.filter(wager=Wager.objects.get(pk=wager_id))
    qlist=list()
    for question in questions:
        qlist.append(question.question)
    labels = iter(qlist)
    WagerAnswerFormSet = formset_factory(WagerAnswerForm, extra=0,
                                              min_num=len(qlist), max_num=len(qlist))

    WagerAnswerFormSet.form = staticmethod(curry(WagerAnswerForm, item_iterator=labels))
    if request.method == "POST":

        formset = WagerAnswerFormSet(request.POST, request.FILES)

        if formset.is_valid():
            question = list(questions)
            i=0
            for form in formset:
                    question[i].answer = form.cleaned_data['answer']
                    question[i].save()
                    i+=1
            wager = Wager.objects.get(pk=wager_id)
            wager.questions_answered = 'true'
            wager.save()
            return redirect('wagers')
        else:
            return redirect('index')
    else:
        formset = WagerAnswerFormSet()
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new = -1
    return render(request, 'par/answer-questions.html', {'new':new, 'formset': formset, })


@login_required
def check_questions(request, wager_id):
    questions = WagerQuestion.objects.filter(wager = Wager.objects.get(pk=wager_id))

    WagerCheckFormSet = formset_factory(WagerCheckForm, extra=0, min_num=len(questions), max_num=len(questions))
    if request.method == "POST":
        formset = WagerCheckFormSet(request.POST, request.FILES)
        i=0
        if formset.is_valid():
            qlist = list(questions)
            for form in formset:
                qlist[i].correct = form.cleaned_data['correct']
                qlist[i].save()
                i+=1
            wager = Wager.objects.get(pk=wager_id)
            wager.questions_checked = 'true'
            for question in questions:
                if question.correct == True:
                    wager.questions_right+=1
            if wager.questions_right/(10-wager.questions)>=0.7:
                wager.winner = 'r'
            else:
                wager.winner = 's'
            wager.save()
            return redirect('wagers')
        else:
            return redirect('index')
    else:
        formset = WagerCheckFormSet()
    if request.user.is_authenticated:
        user = request.user
        new = check_new_wagers(user)
    else:
        new = -1
    return render(request, 'par/check.html', {'new':new, 'formsets': zip(questions, formset), 'formset': formset})


def errors(request):
    return render(request, 'par/errors.html')