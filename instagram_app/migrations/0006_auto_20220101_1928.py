# Generated by Django 3.2.10 on 2022-01-02 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_app', '0005_auto_20220101_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='posts',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='comments',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='posts',
            new_name='post',
        ),
    ]
