# Generated by Django 2.0.1 on 2018-03-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0043_auto_20180322_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='wager',
            name='winner',
            field=models.CharField(default='none', max_length=5),
        ),
    ]
