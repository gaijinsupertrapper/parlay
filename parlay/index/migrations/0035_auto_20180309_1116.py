# Generated by Django 2.0.1 on 2018-03-09 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0034_auto_20180308_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='wager',
            name='new_bet',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='wager',
            name='new_duration',
            field=models.DurationField(null=True),
        ),
    ]
