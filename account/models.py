from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profiles', max_length=250, default='profiles/default.jpg')
    contact = models.CharField(max_length=50, blank=True)
    gender = models.CharField(choices=GENDER, max_length=250, blank=True)
    about = models.TextField(blank=True)
    profession = models.CharField(max_length=50, blank=True)
    linkedIn = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
