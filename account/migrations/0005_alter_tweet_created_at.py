# Generated by Django 3.2.8 on 2022-07-07 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_tweet_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='投稿日時'),
        ),
    ]
