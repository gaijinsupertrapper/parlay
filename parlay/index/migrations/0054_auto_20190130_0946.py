# Generated by Django 2.1.5 on 2019-01-30 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0053_auto_20190130_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='wager',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='wager',
            name='new_duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='wager',
            name='received_new_duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='wager',
            name='sender_new_duration',
            field=models.IntegerField(null=True),
        ),
    ]