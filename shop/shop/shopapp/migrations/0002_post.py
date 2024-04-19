# Generated by Django 5.0.3 on 2024-03-30 13:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=90)),
                ('topic', models.CharField(max_length=10)),
                ('date', models.DateTimeField(verbose_name=datetime.datetime(2024, 3, 30, 13, 13, 18, 272757))),
                ('author', models.TextField()),
            ],
        ),
    ]
