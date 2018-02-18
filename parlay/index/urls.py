from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('book/<int:book_id>/', views.bdetail, name='detail-book'),
    path(r'^signup/$', views.signup, name='signup'),
    path('id<int:user_id>/',views.profile, name='profile'),
    path('id<int:user_id>/edit', views.edit_profile, name = 'edit-profile'),
    path(r'book/<int:book_id>/add', views.add_book, name = 'add-book'),
]