# Generated by Django 3.2.19 on 2023-06-24 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatroom_is_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroommessage',
            name='is_post',
            field=models.BooleanField(default=False),
        ),
    ]