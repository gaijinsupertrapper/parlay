from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Book(models.Model):
    title = models.CharField(max_length = 150, default = r'Yet another book')
    author = models.CharField(max_length = 100, default = r'By yet another author')
    release = models.DateField()
    description = models.TextField(default = r'Description for the book')
    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, default='')
    tokens  = models.IntegerField(default=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    books_read = models.ManyToManyField(Book,)
    friends = models.ManyToManyField(User,  related_name='+',)


class Wager(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='getter')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='none')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


