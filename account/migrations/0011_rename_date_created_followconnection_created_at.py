# Generated by Django 3.2.7 on 2022-07-20 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_followconnection_follow_connection_unique'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followconnection',
            old_name='date_created',
            new_name='created_at',
        ),
    ]
