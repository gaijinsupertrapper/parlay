from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('book/<int:book_id>/', views.bdetail, name='detail-book'),
    path(r'signup', views.signup, name='signup'),
    path('id<int:user_id>/', views.profile, name='profile'),
    path('id<int:user_id>/edit', views.edit_profile, name = 'edit-profile'),
    path(r'book/<int:book_id>/add', views.add_book, name = 'add-book'),
    path('id<int:user_id>/add', views.add_friend, name = 'add-friend'),
    path('id<int:user_id>/remove', views.remove_friend, name = 'remove-friend'),
    path('wagers/add/', views.add_wager, name = 'add-wager'),
    path('wagers/', views.wagers, name='wagers'),
    path('wagers/<int:wager_id>/edit', views.edit_wager, name='edit-wager'),
    path('wagers/<int:wager_id>/accept', views.accept_wager, name = 'accept-wager'),
    path('wagers/<int:wager_id>/decline', views.decline_wager, name = 'decline-wager'),
    path('wagers/<int:wager_id>/end', views.end_wager, name = 'end-wager'),
    path('wagers/<int:wager_id>/reward', views.win_wager, name='win-wager'),
    path('wagers/<int:wager_id>/questions', views.add_questions, name='add-questions'),
    path('id<int:user_id>/friends', views.friends_list, name="friends-list"),
    path('id<int:user_id>/books', views.books_list, name="books-list"),
    path('search/', views.search, name="search"),
    path('q=<str:search_query>', views.search_results, name="search-results"),
    path('book/add/', views.create_book, name="add-book"),
    path('book/error', views.parse_errors, name='parse-errors'),
    path('wager/<int:wager_id>/questions', views.view_questions, name='questions'),
    path('wager/<int:wager_id>/answer', views.answer_questions, name='answer-questions'),
    path('wager/<int:wager_id>/check', views.check_questions, name='check-questions'),
    path('special/add_author', views.add_author, name="add-author")
]


