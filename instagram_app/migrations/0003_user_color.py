# Generated by Django 3.2.19 on 2023-06-04 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_app', '0002_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='color',
            field=models.CharField(default='#ff2f00', max_length=10),
        ),
    ]
