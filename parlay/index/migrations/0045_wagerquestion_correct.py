# Generated by Django 2.0.1 on 2018-03-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0044_wager_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='wagerquestion',
            name='correct',
            field=models.NullBooleanField(),
        ),
    ]