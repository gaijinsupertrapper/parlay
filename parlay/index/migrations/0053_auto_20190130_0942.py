# Generated by Django 2.1.5 on 2019-01-30 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0052_profile_streak'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wager',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='wager',
            name='new_duration',
        ),
        migrations.RemoveField(
            model_name='wager',
            name='received_new_duration',
        ),
        migrations.RemoveField(
            model_name='wager',
            name='sender_new_duration',
        ),
    ]