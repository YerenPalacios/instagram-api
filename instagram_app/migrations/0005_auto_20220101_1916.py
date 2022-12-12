# Generated by Django 3.2.10 on 2022-01-02 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_app', '0004_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.CreateModel(
            name='images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/posts')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instagram_app.post')),
            ],
        ),
    ]
