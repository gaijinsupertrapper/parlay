# Generated by Django 2.1.5 on 2019-01-27 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0049_auto_20180416_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.IntegerField(default=0),
        ),
    ]