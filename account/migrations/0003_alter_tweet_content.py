# Generated by Django 3.2.8 on 2022-06-30 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_tweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.CharField(max_length=255, verbose_name='content'),
        ),
    ]
