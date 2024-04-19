from django.db import models
from django.contrib.auth.models import AbstractUser


class NoteUser(AbstractUser):
    code = models.CharField(max_length=5, default=66666)
    def create_user(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.save()


class Post(models.Model):
    image = models.TextField()
    title = models.CharField(max_length=10)
    text = models.TextField(max_length=90)
    topic = models.CharField(max_length=10)
    date = models.DateTimeField()
    author = models.TextField()

    def create_post(self, image, title, text, topic, date, author):
        self.image = image
        self.title = title
        self.text = text
        self.topic = topic
        self.date = date
        self.author = author
        self.save()
