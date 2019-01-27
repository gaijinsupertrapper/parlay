from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from cloudinary.models import CloudinaryField

class Book(models.Model):
    title = models.CharField(max_length = 150, default = r'Yet another book')
    author = models.CharField(max_length = 100, default = r'By yet another author')
    url = models.URLField(max_length=200, blank=True)
    description = models.TextField(default = r'Description for the book')
    cover_url=models.URLField(max_length=200, blank=True)
    read_by = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, default='')
    favourite_genres = models.CharField(max_length=200, blank=True)
    favourite_authors = models.CharField(max_length=200,blank=True)
    favourite_books = models.CharField(max_length=200,blank=True)
    tokens  = models.IntegerField(default=100)
    avatar = CloudinaryField('image')
    books_read = models.ManyToManyField(Book,)
    books_added = models.IntegerField(default=0)
    friends = models.ManyToManyField(User,  related_name='+',)
    experience = models.IntegerField(default=0)
    next_experience = models.IntegerField(default=100)
    level = models.CharField(max_length=80, default = "Новичок")
    streak = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)


class Wager(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='getter')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='none')
    duration = models.DurationField(null=True)
    until = models.DateTimeField(null=True)
    bet = models.IntegerField(default=5)
    new_duration = models.DurationField(null=True)
    new_bet = models.IntegerField(null=True)
    sender_new_bet = models.IntegerField(null=True)
    sender_new_duration = models.DurationField(null=True)
    received_new_bet = models.IntegerField(null=True)
    received_new_duration = models.DurationField(null=True)
    received_end = models.CharField(max_length=10, default='no')
    sender_end = models.CharField(max_length=10, default='no')
    received_discuss = models.CharField(max_length=10, default='no')
    sender_discuss = models.CharField(max_length=10, default='no')
    questions = models.IntegerField(default=10)
    questions_answered = models.CharField(max_length=10, default='false')
    questions_checked = models.CharField(max_length=10, default='false')
    questions_right = models.IntegerField(default=0)
    winner = models.CharField(max_length=5, default='none')

class WagerQuestion(models.Model):
    wager = models.ForeignKey(Wager, on_delete=models.CASCADE)
    question = models.CharField(max_length=150, default=r'')
    answer = models.CharField(max_length=150, default=r'')
    correct = models.NullBooleanField(null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


