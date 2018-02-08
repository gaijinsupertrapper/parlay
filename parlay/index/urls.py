from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('book/<int:book_id>/', views.bdetail, name='detail-book'),
    path(r'^signup/$', views.signup, name='signup'),

]