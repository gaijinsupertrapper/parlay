# Generated by Django 2.0.1 on 2018-04-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0047_wager_questions_answered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wagerquestion',
            name='answer',
            field=models.CharField(default=' ', max_length=150),
        ),
        migrations.AlterField(
            model_name='wagerquestion',
            name='question',
            field=models.CharField(default=' ', max_length=150),
        ),
    ]
