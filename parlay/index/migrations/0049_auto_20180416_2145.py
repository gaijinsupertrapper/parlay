# Generated by Django 2.0.1 on 2018-04-16 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0048_auto_20180416_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wagerquestion',
            name='answer',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='wagerquestion',
            name='question',
            field=models.CharField(default='', max_length=150),
        ),
    ]