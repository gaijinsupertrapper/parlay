# Generated by Django 2.0.1 on 2018-03-02 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0028_auto_20180302_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wager',
            name='bet',
            field=models.IntegerField(default=5),
        ),
    ]