# Generated by Django 2.0.1 on 2018-03-03 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0030_auto_20180302_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='read_by',
            field=models.BigIntegerField(default=0),
        ),
    ]
